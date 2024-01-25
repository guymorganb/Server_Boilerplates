package com.writerelief.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document // This annotation identifies it as a document stored in MongoDB it represents a
          // document in your MongoDB database.
public class Letter {

    private String id;

    private String content; // Example field

    // Constructors, getters, and setters

    public Letter() {
    }

    public Letter(String id, String content) {
        this.id = id;
        this.content = content;
    }

    // Getters and setters for all fields

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}