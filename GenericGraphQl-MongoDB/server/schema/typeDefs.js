import { gql } from "apollo-server-express";


const typeDefs = gql` #graphql
  type Query {
    hello: String
  }
`;

export default typeDefs;