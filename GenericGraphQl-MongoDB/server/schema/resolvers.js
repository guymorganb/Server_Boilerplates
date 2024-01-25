//import { signToken } from '../utils/authenticate'
//import { AuthenticationError } from 'apollo-server-express'

// require relevant models

const resolvers = {
    Query: {
      hello: () => 'Hello, world!'
    }
  };
  
  export default resolvers;
  