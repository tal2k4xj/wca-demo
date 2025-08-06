package com.example.app.dto;

import com.example.app.model.Customer;
import com.example.app.model.Customer.CustomerType;
import java.math.BigDecimal;
import java.util.Date;

public class CustomerDTO {
    private Integer id;
    private String name;
    private String email;
    private String address;
    private String phone;
    private Date registrationDate;
    private String type;
    private boolean active;
    private BigDecimal creditLimit;
    private int loyaltyPoints;
    private String notes;
    private Date lastPurchaseDate;
    private String preferredContactMethod;
    private int discountPercent;
    private boolean eligibleForUpgrade;

    // Default constructor
    public CustomerDTO() {}

    // Constructor from Customer entity
    public CustomerDTO(Customer customer) {
        this.id = customer.getId();
        this.name = customer.getName();
        this.email = customer.getEmail();
        this.address = customer.getAddress();
        this.phone = customer.getPhone();
        this.registrationDate = customer.getRegistrationDate();
        this.type = customer.getType().name();
        this.active = customer.isActive();
        this.creditLimit = customer.getCreditLimit();
        this.loyaltyPoints = customer.getLoyaltyPoints();
        this.notes = customer.getNotes();
        this.lastPurchaseDate = customer.getLastPurchaseDate();
        this.preferredContactMethod = customer.getPreferredContactMethod();
        this.discountPercent = customer.getDiscountPercent();
        this.eligibleForUpgrade = customer.isEligibleForUpgrade();
    }

    // Convert to Customer entity
    public Customer toCustomer() {
        Customer customer = new Customer();
        customer.setId(this.id);
        customer.setName(this.name);
        customer.setEmail(this.email);
        customer.setAddress(this.address);
        customer.setPhone(this.phone);
        customer.setRegistrationDate(this.registrationDate);
        customer.setType(CustomerType.valueOf(this.type));
        customer.setActive(this.active);
        customer.setCreditLimit(this.creditLimit);
        customer.setLoyaltyPoints(this.loyaltyPoints);
        customer.setNotes(this.notes);
        customer.setLastPurchaseDate(this.lastPurchaseDate);
        customer.setPreferredContactMethod(this.preferredContactMethod);
        return customer;
    }

    // Getters and Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }
    
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    
    public Date getRegistrationDate() { return registrationDate; }
    public void setRegistrationDate(Date registrationDate) { this.registrationDate = registrationDate; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
    
    public BigDecimal getCreditLimit() { return creditLimit; }
    public void setCreditLimit(BigDecimal creditLimit) { this.creditLimit = creditLimit; }
    
    public int getLoyaltyPoints() { return loyaltyPoints; }
    public void setLoyaltyPoints(int loyaltyPoints) { this.loyaltyPoints = loyaltyPoints; }
    
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    
    public Date getLastPurchaseDate() { return lastPurchaseDate; }
    public void setLastPurchaseDate(Date lastPurchaseDate) { this.lastPurchaseDate = lastPurchaseDate; }
    
    public String getPreferredContactMethod() { return preferredContactMethod; }
    public void setPreferredContactMethod(String preferredContactMethod) { 
        this.preferredContactMethod = preferredContactMethod; 
    }
    
    public int getDiscountPercent() { return discountPercent; }
    public void setDiscountPercent(int discountPercent) { this.discountPercent = discountPercent; }
    
    public boolean isEligibleForUpgrade() { return eligibleForUpgrade; }
    public void setEligibleForUpgrade(boolean eligibleForUpgrade) { this.eligibleForUpgrade = eligibleForUpgrade; }
} 