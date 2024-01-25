import express  from "express";
import { ApolloServer } from "apollo-server-express";
import { config } from "dotenv";
import path from "path";
import typeDefs from './schema/typeDefs.js'
import resolvers from './schema/resolvers.js'
//import { auth } from './utils/authenticate.js'
import connectDB from './config/connection.js'

config();

const app = express();
const PORT = process.env.PORT || 3001

// setting for apollo server
const server = new ApolloServer({ 
    typeDefs, 
    resolvers, 
    persistedQueries: false,
    cache: 'bounded',
    //context: auth, //sets the context so the auth middleware
  });

  // Express Middleware
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

(async () => {
    try {
        // Connect to MongoDB
      await connectDB();
      
        // Apollo Server setup
      await server.start();
      server.applyMiddleware({ app });
        
      // Serve static assets in production
      if (process.env.NODE_ENV === 'production') {
        app.use(express.static(path.join(__dirname, '../client/build')));
        
        app.get('*', (req, res) => {
          res.sendFile(path.join(__dirname, '../client/build/index.html'));
        });
      }
  
      
      // Start the server
      app.listen(PORT, () => {
        console.log(`Express server running on port 🔑 ${PORT}!`);
        console.log(`Use GraphQL at ⭐ http://localhost:${PORT}${server.graphqlPath}`);
      });
      
    } catch (error) {
      console.error('Error during server startup:', error);
    }
  })();