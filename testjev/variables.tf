variable "region" {
  default = "ap-northeast-2"
}

# variable "map_accounts" {
#   description = "Additional AWS account numbers to add to the aws-auth configmap."
#   type        = list(string)

#   #   default = [
#   #     "165776267515"
#   #   ]
# }

# variable "map_roles" {
#   description = "Additional IAM roles to add to the aws-auth configmap."
#   type = list(object({
#     rolearn  = string
#     username = string
#     groups   = list(string)
#   }))

#   #   default = [
#   #     {
#   #       rolearn  = "arn:aws:iam::66666666666:role/role1"
#   #       username = "role1"
#   #       groups   = ["system:masters"]
#   #     },
#   #   ]
# }

# variable "map_users" {
#   description = "Additional IAM users to add to the aws-auth configmap."
#   type = list(object({
#     userarn  = string
#     username = string
#     groups   = list(string)
#   }))

#   #   default = [
#   #     {
#   #       userarn  = "arn:aws:iam::165776267515:user/EV"
#   #       username = "EV"
#   #       groups   = ["system:masters"]
#   #     }
#   #   ]
# }