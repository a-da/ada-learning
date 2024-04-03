terraform {

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

resource "aws_instance" "example_server" {

  ami = "ami-098efcc0d4f80810e" # important to match ami with the region !
  instance_type = "t2.micro"

  tags = {
    Name = "ada-learning-terraform"
  }
}
