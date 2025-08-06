IDENTIFICATION DIVISION.
       PROGRAM-ID. CLAIMSPROC.
       AUTHOR. INSURANCE-TEAM.
       DATE-WRITTEN. 2024-03-15.
       
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-ZOS.
       OBJECT-COMPUTER. IBM-ZOS.
       
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CLAIMS-FILE
               ASSIGN TO CLAIMDD
               ORGANIZATION IS INDEXED
               ACCESS MODE IS DYNAMIC
               RECORD KEY IS CLAIM-ID
               FILE STATUS IS WS-CLAIMS-STATUS.
               
           SELECT POLICY-FILE
               ASSIGN TO POLDD
               ORGANIZATION IS INDEXED
               ACCESS MODE IS RANDOM
               RECORD KEY IS POL-ID
               FILE STATUS IS WS-POLICY-STATUS.
               
           SELECT SAS-INPUT
               ASSIGN TO SASINDD
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-SAS-IN-STATUS.
               
           SELECT SAS-OUTPUT
               ASSIGN TO SASOUTDD
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-SAS-OUT-STATUS.
               
           SELECT ERROR-FILE
               ASSIGN TO ERRDD
               ORGANIZATION IS LINE SEQUENTIAL.
               
           SELECT REPORT-FILE
               ASSIGN TO RPTDD
               ORGANIZATION IS LINE SEQUENTIAL.
           
       DATA DIVISION.
       FILE SECTION.
       FD  CLAIMS-FILE.
       01  CLAIM-RECORD.
           05  CLAIM-ID        PIC X(10).
           05  CLAIM-DATE      PIC X(8).
           05  POLICY-ID       PIC X(5).
           05  CLAIM-AMOUNT    PIC 9(7)V99.
           05  CLAIM-TYPE      PIC X(2).
               88  AUTO-CLAIM    VALUE 'AU'.
               88  HOME-CLAIM    VALUE 'HO'.
               88  LIFE-CLAIM    VALUE 'LF'.
           05  STATUS-CODE     PIC X(1).
               88  PENDING       VALUE 'P'.
               88  APPROVED      VALUE 'A'.
               88  REJECTED      VALUE 'R'.
           05  PROCESSOR-ID    PIC X(5).
           05  FILLER          PIC X(10).
           
       FD  POLICY-FILE.
       01  POLICY-RECORD.
           05  POL-ID          PIC X(5).
           05  POL-TYPE        PIC X(2).
           05  CUSTOMER-ID     PIC X(10).
           05  EFFECTIVE-DATE  PIC X(8).
           05  EXPIRY-DATE     PIC X(8).
           05  PREMIUM-AMOUNT  PIC 9(7)V99.
           05  DEDUCTIBLE-AMT  PIC 9(5)V99.
           05  POL-STATUS      PIC X(1).
               88  ACTIVE        VALUE 'A'.
               88  LAPSED        VALUE 'L'.
               88  CANCELLED     VALUE 'C'.
           
       FD  SAS-INPUT.
       01  SAS-IN-RECORD.
           05  SAS-CLAIM-ID    PIC X(10).
           05  SAS-POL-ID      PIC X(5).
           05  SAS-CLAIM-AMT   PIC 9(7)V99.
           05  SAS-CLAIM-TYPE  PIC X(2).
           05  SAS-POL-TYPE    PIC X(2).
           05  SAS-DEDUCT-AMT  PIC 9(5)V99.
           
       FD  SAS-OUTPUT.
       01  SAS-OUT-RECORD.
           05  SAS-OUT-CLAIM-ID  PIC X(10).
           05  SAS-CALC-DEDUCT   PIC 9(5)V99.
           05  SAS-PAID-AMOUNT   PIC 9(7)V99.
           05  SAS-DENIAL-CODE   PIC X(2).
           
       FD  ERROR-FILE.
       01  ERROR-RECORD        PIC X(80).
           
       FD  REPORT-FILE.
       01  REPORT-RECORD       PIC X(132).
       
       WORKING-STORAGE SECTION.
       01  WS-FILE-STATUS.
           05  WS-CLAIMS-STATUS  PIC XX.
           05  WS-POLICY-STATUS  PIC XX.
           05  WS-SAS-IN-STATUS  PIC XX.
           05  WS-SAS-OUT-STATUS PIC XX.
           
       01  WS-COUNTERS.
           05  WS-READ-COUNT     PIC 9(7) VALUE 0.
           05  WS-ERROR-COUNT    PIC 9(5) VALUE 0.
           05  WS-PROCESS-COUNT  PIC 9(7) VALUE 0.
           
       01  WS-TOTALS.
           05  WS-TOTAL-CLAIMS   PIC 9(9)V99 VALUE 0.
           05  WS-TOTAL-PAID     PIC 9(9)V99 VALUE 0.
           
       01  WS-DATE-TIME.
           05  WS-CURRENT-DATE   PIC X(8).
           05  WS-CURRENT-TIME   PIC X(6).
           
       01  WS-FLAGS.
           05  WS-EOF-CLAIMS     PIC X VALUE 'N'.
               88  END-OF-CLAIMS   VALUE 'Y'.
           05  WS-VALID-POLICY   PIC X VALUE 'N'.
               88  POLICY-VALID    VALUE 'Y'.
           
       01  WS-SAS-COMMAND.
           05  FILLER            PIC X(30) 
               VALUE 'sas -sysin process_claims.sas '.
           05  FILLER            PIC X(15)
               VALUE '-log sas.log '.
           05  FILLER            PIC X(35)
               VALUE '-print claims_report.lst -noterminal'.
           
       PROCEDURE DIVISION.
       0000-MAIN.
           PERFORM 1000-INITIALIZE
           PERFORM 2000-PROCESS-CLAIMS
           PERFORM 3000-CALL-SAS
           PERFORM 4000-PROCESS-RESULTS
           PERFORM 5000-CLEANUP
           STOP RUN.
           
       1000-INITIALIZE.
           ACCEPT WS-CURRENT-DATE FROM DATE YYYYMMDD
           ACCEPT WS-CURRENT-TIME FROM TIME
           
           OPEN INPUT CLAIMS-FILE
               OUTPUT SAS-INPUT
               OUTPUT ERROR-FILE
               OUTPUT REPORT-FILE
               I-O POLICY-FILE
               
           IF WS-CLAIMS-STATUS NOT = '00'
               DISPLAY 'CLAIMS FILE ERROR: ' WS-CLAIMS-STATUS
               PERFORM 9999-ABORT
           END-IF.
           
       2000-PROCESS-CLAIMS.
           PERFORM UNTIL END-OF-CLAIMS
               READ CLAIMS-FILE
                   AT END
                       SET END-OF-CLAIMS TO TRUE
                   NOT AT END
                       ADD 1 TO WS-READ-COUNT
                       PERFORM 2100-VALIDATE-CLAIM
               END-READ
           END-PERFORM.
           
       2100-VALIDATE-CLAIM.
           INITIALIZE WS-VALID-POLICY
           
           IF CLAIM-AMOUNT <= ZERO
               PERFORM 2900-WRITE-ERROR
               GO TO 2100-EXIT
           END-IF
           
           MOVE POLICY-ID TO POL-ID
           READ POLICY-FILE
               INVALID KEY
                   PERFORM 2900-WRITE-ERROR
               NOT INVALID KEY
                   IF ACTIVE
                       SET POLICY-VALID TO TRUE
                       PERFORM 2200-WRITE-SAS-INPUT
                   ELSE
                       PERFORM 2900-WRITE-ERROR
                   END-IF
           END-READ.
           
       2200-WRITE-SAS-INPUT.
           MOVE CLAIM-ID TO SAS-CLAIM-ID
           MOVE POLICY-ID TO SAS-POL-ID
           MOVE CLAIM-AMOUNT TO SAS-CLAIM-AMT
           MOVE CLAIM-TYPE TO SAS-CLAIM-TYPE
           MOVE POL-TYPE TO SAS-POL-TYPE
           MOVE DEDUCTIBLE-AMT TO SAS-DEDUCT-AMT
           
           WRITE SAS-IN-RECORD
           ADD 1 TO WS-PROCESS-COUNT.
           
       2900-WRITE-ERROR.
           ADD 1 TO WS-ERROR-COUNT
           MOVE SPACES TO ERROR-RECORD
           STRING 'INVALID CLAIM - ID: ' CLAIM-ID
                  ' POLICY: ' POLICY-ID
                  ' DATE: ' CLAIM-DATE
                  INTO ERROR-RECORD
           WRITE ERROR-RECORD.
           
       3000-CALL-SAS.
           IF WS-PROCESS-COUNT > 0
               CALL "SYSTEM" USING WS-SAS-COMMAND
               IF RETURN-CODE NOT = 0
                   DISPLAY 'SAS PROCESSING ERROR'
                   PERFORM 9999-ABORT
               END-IF
           END-IF.
           
       4000-PROCESS-RESULTS.
           OPEN INPUT SAS-OUTPUT
           
           PERFORM UNTIL WS-SAS-OUT-STATUS = '10'
               READ SAS-OUTPUT
                   AT END
                       CONTINUE
                   NOT AT END
                       PERFORM 4100-UPDATE-CLAIM
               END-READ
           END-PERFORM
           
           CLOSE SAS-OUTPUT.
           
       4100-UPDATE-CLAIM.
           MOVE SAS-OUT-CLAIM-ID TO CLAIM-ID
           READ CLAIMS-FILE
               INVALID KEY
                   PERFORM 2900-WRITE-ERROR
               NOT INVALID KEY
                   IF SAS-DENIAL-CODE = SPACES
                       MOVE 'A' TO STATUS-CODE
                       ADD SAS-PAID-AMOUNT TO WS-TOTAL-PAID
                   ELSE
                       MOVE 'R' TO STATUS-CODE
                   END-IF
                   REWRITE CLAIM-RECORD
           END-READ.
           
       5000-CLEANUP.
           PERFORM 5100-WRITE-REPORT
           
           CLOSE CLAIMS-FILE
                 POLICY-FILE
                 SAS-INPUT
                 ERROR-FILE
                 REPORT-FILE.
           
       5100-WRITE-REPORT.
           MOVE SPACES TO REPORT-RECORD
           STRING 'CLAIMS PROCESSING REPORT - ' WS-CURRENT-DATE
                  ' ' WS-CURRENT-TIME
                  INTO REPORT-RECORD
           WRITE REPORT-RECORD
           
           MOVE SPACES TO REPORT-RECORD
           STRING 'TOTAL CLAIMS READ:    ' WS-READ-COUNT
                  INTO REPORT-RECORD
           WRITE REPORT-RECORD
           
           MOVE SPACES TO REPORT-RECORD
           STRING 'CLAIMS PROCESSED:     ' WS-PROCESS-COUNT
                  INTO REPORT-RECORD
           WRITE REPORT-RECORD
           
           MOVE SPACES TO REPORT-RECORD
           STRING 'ERRORS ENCOUNTERED:   ' WS-ERROR-COUNT
                  INTO REPORT-RECORD
           WRITE REPORT-RECORD
           
           MOVE SPACES TO REPORT-RECORD
           STRING 'TOTAL AMOUNT PAID:    ' WS-TOTAL-PAID
                  INTO REPORT-RECORD
           WRITE REPORT-RECORD.
           
       9999-ABORT.
           DISPLAY 'ABNORMAL TERMINATION'
           MOVE 16 TO RETURN-CODE
           STOP RUN.
           
       2100-EXIT.
           EXIT.