/* Process claims with business rules */
DATA claims;
    INFILE 'sas_in.dat' PAD;
    INPUT @1  claim_date    $8.
          @9  policy_id     $5.
          @14 claim_amount  7.2;
    
    /* Apply deductible business rule */
    IF claim_amount <= 1000 THEN deductible = 100;
    ELSE IF claim_amount <= 5000 THEN deductible = 250;
    ELSE deductible = 500;
    
    amount_paid = claim_amount - deductible;
RUN;

/* Write summary back for COBOL */
DATA _NULL_;
    SET claims;
    FILE 'sas_out.dat';
    PUT @1  policy_id     $5.
        @6  deductible    7.2
        @13 amount_paid   9.2;
RUN;