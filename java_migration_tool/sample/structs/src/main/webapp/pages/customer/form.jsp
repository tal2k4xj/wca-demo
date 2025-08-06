
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html" %>

<html>
<head><title>Customer Form</title></head>
<body>
    <h1>Customer Form</h1>
    <html:form action="/customer">
        <html:text property="name"/>
        <html:errors property="name"/>
    </html:form>
</body>
</html>
