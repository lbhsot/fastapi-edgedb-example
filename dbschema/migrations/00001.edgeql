CREATE MIGRATION m16vq3jx6swyju7yjzk32ggmysrubxhf5ri4dn4ds6oosxvjpq23jq
    ONTO initial
{
  CREATE TYPE default::User {
      CREATE REQUIRED PROPERTY username -> std::str;
  };
};
