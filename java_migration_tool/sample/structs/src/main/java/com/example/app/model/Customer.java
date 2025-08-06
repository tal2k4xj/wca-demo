package com.example.app.model;

import java.util.Date;
import java.math.BigDecimal;

public class Customer {
    private Long id;
    private String name;
    private String email;
    private String address;
    private String phone;
    private Date createdDate;
    private CustomerType type;
    private boolean active;
    private BigDecimal creditLimit;
    private int loyaltyPoints;
    private String notes;
    private Date lastPurchaseDate;
    private String preferredContactMethod;

    public enum CustomerType {
        REGULAR("Regular Customer", 0),
        PREMIUM("Premium Member", 10),
        VIP("VIP Member", 20),
        CORPORATE("Corporate Account", 15);

        private final String displayName;
        private final int discountPercent;

        CustomerType(String displayName, int discountPercent) {
            this.displayName = displayName;
            this.discountPercent = discountPercent;
        }

        public String getDisplayName() { return displayName; }
        public int getDiscountPercent() { return discountPercent; }
    }

    public Customer() {
        this.createdDate = new Date();
        this.active = true;
        this.type = CustomerType.REGULAR;
        this.creditLimit = BigDecimal.ZERO;
        this.loyaltyPoints = 0;
        this.preferredContactMethod = "EMAIL";
    }

    public Customer(Long id, String name, String email, String address) {
        this();
        this.id = id;
        this.name = name;
        this.email = email;
        this.address = address;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public String getAddress() {
        return address;
    }
    
    public void setAddress(String address) {
        this.address = address;
    }
    
    public String getPhone() {
        return phone;
    }
    
    public void setPhone(String phone) {
        this.phone = phone;
    }
    
    public Date getCreatedDate() {
        return createdDate;
    }
    
    public void setCreatedDate(Date createdDate) {
        this.createdDate = createdDate;
    }
    
    public CustomerType getType() {
        return type;
    }
    
    public void setType(CustomerType type) {
        this.type = type;
    }
    
    public boolean isActive() {
        return active;
    }
    
    public void setActive(boolean active) {
        this.active = active;
    }
    
    public BigDecimal getCreditLimit() {
        return creditLimit;
    }
    
    public void setCreditLimit(BigDecimal creditLimit) {
        this.creditLimit = creditLimit;
    }
    
    public int getLoyaltyPoints() {
        return loyaltyPoints;
    }
    
    public void setLoyaltyPoints(int loyaltyPoints) {
        this.loyaltyPoints = loyaltyPoints;
    }
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    public Date getLastPurchaseDate() {
        return lastPurchaseDate;
    }
    
    public void setLastPurchaseDate(Date lastPurchaseDate) {
        this.lastPurchaseDate = lastPurchaseDate;
    }
    
    public String getPreferredContactMethod() {
        return preferredContactMethod;
    }
    
    public void setPreferredContactMethod(String preferredContactMethod) {
        this.preferredContactMethod = preferredContactMethod;
    }

    // Business methods
    public boolean isEligibleForUpgrade() {
        return loyaltyPoints >= 1000 && type != CustomerType.VIP;
    }

    public void addLoyaltyPoints(int points) {
        this.loyaltyPoints += points;
    }

    public int getDiscountPercent() {
        return type.getDiscountPercent();
    }

    @Override
    public String toString() {
        return "Customer{" +
               "id=" + id +
               ", name='" + name + '\'' +
               ", email='" + email + '\'' +
               ", type=" + type.getDisplayName() +
               ", loyaltyPoints=" + loyaltyPoints +
               '}';
    }
} 