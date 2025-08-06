package com.example.app.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.example.app.model.Customer;
import com.example.app.form.CustomerForm;

public class CustomerService {
    private static final Map<Long, Customer> customerDb = new HashMap<>();
    private static long idSequence = 1;

    public Customer saveCustomer(CustomerForm form) {
        Customer customer = new Customer();
        customer.setId(form.getId() != null ? form.getId() : idSequence++);
        customer.setName(form.getName());
        customer.setEmail(form.getEmail());
        customer.setPhone(form.getPhone());
        customer.setActive(form.isActive());
        
        customerDb.put(customer.getId(), customer);
        return customer;
    }

    public CustomerForm getCustomerForm(Long id) {
        Customer customer = customerDb.get(id);
        if (customer != null) {
            CustomerForm form = new CustomerForm();
            form.setId(customer.getId());
            form.setName(customer.getName());
            form.setEmail(customer.getEmail());
            form.setPhone(customer.getPhone());
            form.setActive(customer.isActive());
            return form;
        }
        return null;
    }

    public void deleteCustomer(Long id) {
        customerDb.remove(id);
    }

    public List<Customer> getAllCustomers() {
        return new ArrayList<>(customerDb.values());
    }
} 