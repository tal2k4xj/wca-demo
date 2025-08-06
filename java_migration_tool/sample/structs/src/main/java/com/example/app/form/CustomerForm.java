package com.example.app.form;

import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionMapping;
import org.apache.struts.action.ActionErrors;
import org.apache.struts.action.ActionError;
import javax.servlet.http.HttpServletRequest;

public class CustomerForm extends ActionForm {
    private Long id;
    private String name;
    private String email;
    private String phone;
    private boolean active;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }

    @Override
    public void reset(ActionMapping mapping, HttpServletRequest request) {
        id = null;
        name = null;
        email = null;
        phone = null;
        active = false;
    }

    @Override
    public ActionErrors validate(ActionMapping mapping, HttpServletRequest request) {
        ActionErrors errors = new ActionErrors();
        
        if (name == null || name.trim().isEmpty()) {
            errors.add("name", new ActionError("error.name.required"));
        }
        
        if (email == null || email.trim().isEmpty()) {
            errors.add("email", new ActionError("error.email.required"));
        }
        
        return errors;
    }
}
