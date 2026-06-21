# Redundant DNS Architecture Design for TechKraft

## 1. Architecture Diagram

```text
Users (Nepal / South Asia)
          |
          v
     Route 53 (DNS Layer)
          |
   --------------------------------
   |                              |
Primary Region (ap-south-1)   Secondary Region (ap-southeast-1)
   |                              |
 CloudFront (optional)        CloudFront (optional)
   |                              |
 Application Load Balancer   Application Load Balancer
   |                              |
 EC2 Auto Scaling Group      EC2 Auto Scaling Group
 (Multi-AZ, Private Subnets) (Multi-AZ, Private Subnets)
