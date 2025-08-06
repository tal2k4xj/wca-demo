# WCA General Demo: Modernizing COBOL Applications with Embedded SAS Code
In this demo, we showcase how to use Watsonx Code Assistant (WCA) to modernize COBOL applications that contain embedded SAS programming logic. The demo illustrates the partnership between <span style="color: red;">WCA for Z</span> and <span style="color: blue;">WCA</span> with a step-by-step approach to <span style="color: red;">understanding legacy code, optimizing COBOL, converting to Java</span>, <span style="color: blue;">and handling embedded SAS code translation </span>. This demo is designed for developers working on mainframe modernization projects who need to handle mixed-language codebases.

## Demo Documents:
- [Video](https://ibm-my.sharepoint.com/:v:/p/ashwin_pothukuchi/EbV8Scu-sCRNgHdHN97ftscBVFVMDpTgHO4ERoJr-meblA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=FwN5Lh)
- [Script](https://ibm-my.sharepoint.com/:w:/p/ashwin_pothukuchi/EV8XO7GS6D1Bu06bEeLRa_0Bx1bh2Sl762kpLkN6MLlKrg?e=Xaa21h)
- Instructions - see below
- [Owner Contact - 1](https://ibm.enterprise.slack.com/user/@U042HPTE7NK)
- [Owner Contact - 2](https://ibm.enterprise.slack.com/user/@W3RFYSCPP)

## Set Up Guide
Install the latest version of Watsonx Code Assistant and be familiar with the WCA for Z steps outlined in [this video](https://www.ibm.com/products/watsonx-code-assistant-z?utm_content=SRCWW&p1=Search&p4=43700081200370818&p5=e&p9=58700008820506023&gad_source=1&gclid=Cj0KCQiAvvO7BhC-ARIsAGFyToUYGvMW5Jhmat4qKeAFfXTrm0RZ7PK6mxKtmOX5bYvR8XJMBdDHFqUaAoKaEALw_wcB&gclsrc=aw.ds)

This demo does not require a WCA for Z environment and can re-use clips from either video to explain that component if necessary. We are assuming that the COBOL has been converted to mainframe Java and that we now need to understand and translate a SAS script that held some business logic and read a shared data file with the COBOL application.

#### Install latest version of Watsonx Code Assistants:
1. For VS Code and Eclipse extensions, follow instructions on [techzone](https://techzone.ibm.com/collection/wca/environments)
2. If you want to demo WCA for Z live or convert custom COBOL, follow the installation guide on [techzone](https://techzone.ibm.com/collection/653fee8bf2cbbb0017e126de)


## File structure

1. `cobol/CLAIMSPROC_LONG.cbl` - original COBOL file (for reference or customization of the demo, not necessary)
2. `sas/deduct.sas` - SAS script that is called by original claim processing COBOL script and reads/writes a shared data file
3. `sas/claims.dat` - Shared data file used by sas script (for reference or customization of the demo, not necessary)
4. `cobol_conversion.java` - Simplified output of the WCA for Z process --  a mainframe java claims processing application

## Instructions to run the demo
The demo commands are very simple once you have you WCA set up and the repo cloned.

1. Start a new chat
2. Enter `/explain @cobol_conversion.java` or click explain on ClaimsProcessor class definition in `cobol_conversion.java`
3. Enter `/explain @deduct.sas`
4. Enter `/translate to java @deduct.sas`
5. *Optional & not thoroughly tested* - Enter  `Can you write a complete Java script that combines the deductible logic in the ClaimsProcessor?`

This last step would show how to then have an independent distributed Java script that has all of the legacy logic (ideally). Feel free to play around wit that last prompt.