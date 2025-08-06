package com.example.app.action;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.struts.action.Action;
import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;
import com.example.app.form.CustomerForm;
import com.example.app.service.CustomerService;

public class CustomerAction extends Action {
    private CustomerService customerService;

    public CustomerAction() {
        customerService = new CustomerService();
    }

    @Override
    public ActionForward execute(ActionMapping mapping, ActionForm form,
            HttpServletRequest request, HttpServletResponse response) throws Exception {
        
        CustomerForm customerForm = (CustomerForm) form;
        String method = request.getParameter("method");
        
        if ("create".equals(method)) {
            return mapping.findForward("form");
        } else if ("save".equals(method)) {
            customerService.saveCustomer(customerForm);
            return mapping.findForward("list");
        } else if ("edit".equals(method)) {
            Long id = Long.parseLong(request.getParameter("id"));
            customerForm = customerService.getCustomerForm(id);
            request.setAttribute("customerForm", customerForm);
            return mapping.findForward("form");
        } else if ("delete".equals(method)) {
            Long id = Long.parseLong(request.getParameter("id"));
            customerService.deleteCustomer(id);
            return mapping.findForward("list");
        }
        
        // Default: show list
        request.setAttribute("customerList", customerService.getAllCustomers());
        return mapping.findForward("list");
    }
}