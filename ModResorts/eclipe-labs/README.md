# Installation guide for wca4ej (This guide is not up to date -- for any demos please refer to the VS Code labs)

This document gives infomration on installing software tools/IDE that are needed to run ***Watson Code Assistant For Enterprise Java*** **(Wca4ej)**
## Environment setup 

### 1. Java installation

#### Install Java21 using this link [Download Java](https://www.oracle.com/sg/java/technologies/downloads/)
- After installing java, add java to `PATH` variable and set `JAVA_HOME` envitonment variable
- Check if Java is installed properly:
```bash
java --version
```

### 2. Install Maven

- Windows
    - Visit the official Maven website: [Maven Download Page](https://maven.apache.org/download.cgi)
    - Under "Files", click on the binary zip archive link (e.g., apache-maven-x.x.x-bin.zip). 
    - Extract the zip file to a location of your choice, e.g., C:\Apache\maven.
    - Add Maven to PATH and Set MAVEN_HOME variable 
- Mac
   - Install maven using homebrew
```bash
brew install maven
```

Check if maven is installed properly:
```bash
mvn --version
```


### 3. Install Eclipse

Eclipse users must install one of these two packages:
   - Eclipse IDE for Java Developers
   - Eclipse IDE for Enterprise Java and Web Developers 

Below are the links for eclipse installation
- [Eclipse 2024-03](https://www.eclipse.org/downloads/packages/release/2024-03/r)
- [Eclipse 2023-12](https://www.eclipse.org/downloads/packages/release/2023-12/r)

Move **Eclipse.app** to **Application** (For Mac)

![screenshot](./images/8.eclipse.png)



### 4. Configure Java21 in Eclipse
If for some reason Eclipse doesn’t automatically detect your Java 21 installation, first try restarting it. Else:

- Go to Window > Preferences (for the windows) **OR** Eclipse > Settings (for the mac).
- Expand the Java section and click on Installed JREs.
- Make sure to select Java21, if already present in the options and click Apply and Close
- Else, Click Add and select Standard VM.
- Browse to the folder where your Java 21 is installed (typically C:\Program Files\Java\jdk-21).
- Select the JDK and click Finish.
![screenshot](./images/9.Configure_Java21_in_Eclipse.png)

### 5. Techzone environment 
You can reserve an instance in techzone by using this [Techzone Link](https://techzone.ibm.com/collection/wca/environments).


After reserving the instance, you can accept the invitation sent to your email and then create an API key using below steps.

1. Go to cloud.ibm.com to create an API key for later use in WCA:
2. Look at the top menu bar and click on Manage > Access (IAM) > API keys.
3. Click Create an IBM Cloud API key.
4. Enter a name and description for your API key.
5. Click Create.
6. Then, click Show to display the API key or click Copy to copy
7. Save this API Key for later entry into the WCA plugin for Eclipse

Next go to cloud.ibm.com/resources and expand the "AI/Machine Learning" group then click on “wca4eja - primary”:

![alt text](./images/image.png)

Click on the Launch watsonx Code Assistant button
![alt text](./images/image-1.png)

If you see the screen below, click Setup.
![alt text](./images/image-2.png)

In the next screen, you can follow the instructions for the first checkmark to create your own Deployment Space:
![alt text](./images/image-3.png)

Ignore the 2nd and 3rd checkmark.  Do not invite users to your IBM Cloud account nor to your Deployment space.

Now, you are ready to use your API key in the Eclipse plugin.


### 6. Download Wca4ej extension

Download the latest WCA4EJ Code Eclipse Extension and install by following these instructions: [Wca4ej Extension](https://early-access.ibm.com/software/support/trial/cst/welcomepage.wss?siteId=2044)

- If using Windows OS, the Windows plugin requires the [Microsoft Edge WebView2 runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/?form=MA13LH). 
- Scroll down and choose Evergreen Standalone Installer. 
- In newer versions of Windows this might already be installed. In that case, you will receive this message while installing.


### 7. Installing Wca4ej extension


#### After downloding the extension from **Step 5** install the wca4ej using eclipse as shown below 
![screenshot](./images/1.InstallNewSw.png)

#### Choose the local package or archive and provide the path where the extension files are downloaded from **Step 4** 
- Enter a name in the Name field, then click **Add**.
- Click the check box for the plugin, then click **Next**.
- On Install Details, review the items, then click **Next**.
- On Review Licenses, read the license, click to agree, then click **Finish**.
- On Trust Artifacts, click the **Type** check box, then click **Trust Selected**.
- **IMPORTANT**: Do not close eclipse until Installing Software progress bar completes in the **right bottom**.
  
![screenshot](./images/2.LocateLocalPackage.png)

![screenshot](./images/10.InstallingSoftwareStatusbar.png)

#### After the software (extension gets installed), restart your Eclipse IDE. After restart, navigate to below setting 

![screenshot](./images/4.ChooseviewEclipse.png)

#### Then choose the 'Chat' feature of Watson code assistant for enterprise java as below

![screenshot](./images/5.ShowWca4ejChatView.png)

#### After this, you will be navigated to below screen [enter the API key generated in Step 5].
![screenshot](./images/3.Wca4ejchat.png)

### 8. Installing Liberty Tools

Install the liberty tools from eclipse market place as shown below [Help >> Eclipse Marketplace]
![screenshot](./images/6.LibertyTools.png)


Now, you can start using wca4ej.


