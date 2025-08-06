package com.insurance.claims;

import java.io.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.logging.*;

public class ClaimsProcessor {
    // Constants
    private static final String CLAIMS_FILE = "CLAIMS.VSAM";
    private static final String POLICY_FILE = "POLICY.VSAM";
    private static final String SAS_INPUT = "SAS.INPUT.DAT";
    private static final String SAS_OUTPUT = "SAS.OUTPUT.DAT";
    private static final String ERROR_FILE = "ERROR.LOG";
    private static final String REPORT_FILE = "CLAIMS.RPT";
    
    // Status codes matching COBOL
    private enum ClaimType {
        AUTO("AU"), HOME("HO"), LIFE("LF");
        private final String code;
        ClaimType(String code) { this.code = code; }
    }
    
    private enum Status {
        PENDING("P"), APPROVED("A"), REJECTED("R");
        private final String code;
        Status(String code) { this.code = code; }
    }
    
    private enum PolicyStatus {
        ACTIVE("A"), LAPSED("L"), CANCELLED("C");
        private final String code;
        PolicyStatus(String code) { this.code = code; }
    }
    
    // Record definitions matching COBOL layouts
    record ClaimRecord(
        String claimId,          // PIC X(10)
        LocalDate claimDate,     // PIC X(8)
        String policyId,         // PIC X(5)
        BigDecimal claimAmount,  // PIC 9(7)V99
        ClaimType claimType,     // PIC X(2)
        Status statusCode,       // PIC X(1)
        String processorId,      // PIC X(5)
        String filler           // PIC X(10)
    ) {
        // Convert to fixed-width format for file I/O
        String toFixedWidth() {
            return String.format("%-10s%-8s%-5s%09.2f%-2s%-1s%-5s%-10s",
                claimId,
                claimDate.format(DateTimeFormatter.BASIC_ISO_DATE),
                policyId,
                claimAmount,
                claimType.code,
                statusCode.code,
                processorId,
                filler);
        }
    }
    
    record PolicyRecord(
        String policyId,         // PIC X(5)
        String policyType,       // PIC X(2)
        String customerId,       // PIC X(10)
        LocalDate effectiveDate, // PIC X(8)
        LocalDate expiryDate,    // PIC X(8)
        BigDecimal premium,      // PIC 9(7)V99
        BigDecimal deductible,   // PIC 9(5)V99
        PolicyStatus status      // PIC X(1)
    ) {}
    
    // Working storage variables
    private static class WorkingStorage {
        int readCount = 0;
        int errorCount = 0;
        int processCount = 0;
        BigDecimal totalClaims = BigDecimal.ZERO;
        BigDecimal totalPaid = BigDecimal.ZERO;
        LocalDateTime processingDateTime;
        private static final Logger logger = Logger.getLogger("ClaimsProcessor");
    }
    
    public static void main(String[] args) {
        WorkingStorage ws = new WorkingStorage();
        try {
            initialize(ws);
            processClaims(ws);
            callSAS(ws);
            processResults(ws);
            cleanup(ws);
        } catch (Exception e) {
            abend("CLAIMS PROCESSING FAILURE", e);
        }
    }
    
    private static void initialize(WorkingStorage ws) throws IOException {
        ws.processingDateTime = LocalDateTime.now();
        
        // Initialize logger
        FileHandler fh = new FileHandler(ERROR_FILE);
        ws.logger.addHandler(fh);
        ws.logger.setLevel(Level.ALL);
        
        // Validate environment
        checkFileAccess(CLAIMS_FILE);
        checkFileAccess(POLICY_FILE);
    }
    
    private static void processClaims(WorkingStorage ws) throws IOException {
        try (VSAMReader<ClaimRecord> claimsFile = new VSAMReader<>(CLAIMS_FILE);
             VSAMReader<PolicyRecord> policyFile = new VSAMReader<>(POLICY_FILE);
             PrintWriter sasInput = new PrintWriter(new FileWriter(SAS_INPUT))) {
            
            ClaimRecord claim;
            while ((claim = claimsFile.read()) != null) {
                ws.readCount++;
                
                if (validateClaim(claim, policyFile, ws)) {
                    writeSASInput(claim, sasInput);
                    ws.processCount++;
                }
            }
        }
    }
    
    private static boolean validateClaim(
            ClaimRecord claim, 
            VSAMReader<PolicyRecord> policyFile, 
            WorkingStorage ws) throws IOException {
        
        // Validate claim amount
        if (claim.claimAmount().compareTo(BigDecimal.ZERO) <= 0) {
            logError(ws, "Invalid claim amount: " + claim.claimId());
            return false;
        }
        
        // Validate policy
        PolicyRecord policy = policyFile.read(claim.policyId());
        if (policy == null) {
            logError(ws, "Policy not found: " + claim.policyId());
            return false;
        }
        
        if (policy.status() != PolicyStatus.ACTIVE) {
            logError(ws, "Policy not active: " + claim.policyId());
            return false;
        }
        
        return true;
    }
    
    private static void writeSASInput(ClaimRecord claim, PrintWriter writer) {
        // Write in fixed-width format for SAS
        writer.println(String.format("%-10s%-5s%09.2f%-2s",
            claim.claimId(),
            claim.policyId(),
            claim.claimAmount(),
            claim.claimType().code));
    }
    
    private static void callSAS(WorkingStorage ws) throws IOException {
        if (ws.processCount > 0) {
            Process sasProcess = Runtime.getRuntime().exec(
                "sas -sysin process_claims.sas -log sas.log -print claims_report.lst -noterminal"
            );
            
            try {
                int exitCode = sasProcess.waitFor();
                if (exitCode != 0) {
                    throw new IOException("SAS processing failed with code: " + exitCode);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new IOException("SAS processing interrupted", e);
            }
        }
    }
    
    private static void processResults(WorkingStorage ws) throws IOException {
        try (VSAMReader<ClaimRecord> claimsFile = new VSAMReader<>(CLAIMS_FILE);
             BufferedReader sasOutput = new BufferedReader(new FileReader(SAS_OUTPUT))) {
            
            String line;
            while ((line = sasOutput.readLine()) != null) {
                String claimId = line.substring(0, 10).trim();
                BigDecimal calculatedDeductible = new BigDecimal(line.substring(10, 17).trim());
                BigDecimal paidAmount = new BigDecimal(line.substring(17, 26).trim());
                String denialCode = line.substring(26, 28).trim();
                
                updateClaim(claimId, paidAmount, denialCode, claimsFile, ws);
            }
        }
    }
    
    private static void updateClaim(
            String claimId, 
            BigDecimal paidAmount, 
            String denialCode,
            VSAMReader<ClaimRecord> claimsFile,
            WorkingStorage ws) throws IOException {
        
        ClaimRecord claim = claimsFile.read(claimId);
        if (claim == null) {
            logError(ws, "Claim not found for update: " + claimId);
            return;
        }
        
        Status newStatus = denialCode.isEmpty() ? Status.APPROVED : Status.REJECTED;
        
        ClaimRecord updatedClaim = new ClaimRecord(
            claim.claimId(),
            claim.claimDate(),
            claim.policyId(),
            claim.claimAmount(),
            claim.claimType(),
            newStatus,
            claim.processorId(),
            claim.filler()
        );
        
        claimsFile.update(updatedClaim);
        
        if (newStatus == Status.APPROVED) {
            ws.totalPaid = ws.totalPaid.add(paidAmount);
        }
    }
    
    private static void cleanup(WorkingStorage ws) throws IOException {
        try (PrintWriter report = new PrintWriter(new FileWriter(REPORT_FILE))) {
            writeReport(report, ws);
        }
    }
    
    private static void writeReport(PrintWriter report, WorkingStorage ws) {
        report.printf("CLAIMS PROCESSING REPORT - %s%n",
            ws.processingDateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        report.printf("TOTAL CLAIMS READ:    %d%n", ws.readCount);
        report.printf("CLAIMS PROCESSED:     %d%n", ws.processCount);
        report.printf("ERRORS ENCOUNTERED:   %d%n", ws.errorCount);
        report.printf("TOTAL AMOUNT PAID:    $%,.2f%n", ws.totalPaid);
    }
    
    private static void logError(WorkingStorage ws, String message) {
        ws.errorCount++;
        ws.logger.warning(message);
    }
    
    private static void abend(String message, Exception e) {
        System.err.println("ABEND: " + message);
        e.printStackTrace();
        System.exit(16);
    }
    
    private static void checkFileAccess(String filename) throws IOException {
        File file = new File(filename);
        if (!file.exists() || !file.canRead()) {
            throw new IOException("Cannot access required file: " + filename);
        }
    }
}

// VSAM file handling simulation
class VSAMReader<T> implements AutoCloseable {
    private final String filename;
    
    public VSAMReader(String filename) {
        this.filename = filename;
    }
    
    public T read() throws IOException {
        // Implement VSAM record reading
        return null;
    }
    
    public T read(String key) throws IOException {
        // Implement VSAM record reading by key
        return null;
    }
    
    public void update(T record) throws IOException {
        // Implement VSAM record update
    }
    
    @Override
    public void close() throws IOException {
        // Close VSAM file
    }
}