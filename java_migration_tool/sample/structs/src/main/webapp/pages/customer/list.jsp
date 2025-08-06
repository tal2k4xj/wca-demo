
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html" %>
<%@ taglib uri="http://struts.apache.org/tags-logic" prefix="logic" %>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean" %>

<html>
<head><title>Customer List</title></head>
<body>
    <h1>Customer List</h1>
    <table>
        <logic:iterate name="customerList" id="customer">
            <tr>
                <td><bean:write name="customer" property="name"/></td>
            </tr>
        </logic:iterate>
    </table>
</body>
</html>
