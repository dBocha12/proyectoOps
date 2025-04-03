terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "example_server" {
  ami           = var.aws_ami
  instance_type = var.aws_instance_type
  key_name      = var.aws_key_name

  vpc_security_group_ids = [aws_security_group.my_sg.id] 

  tags = {
    Name = var.aws_name
  }
}

resource "aws_security_group" "my_sg" {
  name        = "${var.aws_name} - SG"
  description = "SG creado desde Chatops"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}