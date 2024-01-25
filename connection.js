/**
 * Sequelize Connection Config
 */
require('dotenv').config();

const Sequelize = require('sequelize');

let sequelize;

if (process.env.DATABASE_URL) { // This environment variable will be available on Heroku after you've provisioned a PostgreSQL database
    sequelize = new Sequelize(process.env.DATABASE_URL, {
        dialect: 'postgres',
        protocol: 'postgres',
        dialectOptions: {
            ssl: {
                require: true,
                rejectUnauthorized: false // Required for Heroku
            }
        }
    });
} else {
    sequelize = new Sequelize(process.env.POSTGRE_DBNAME, process.env.POSTGRE_USERNAME, String(process.env.POSTGRE_PASS), {
        host: '127.0.0.1',
        dialect: 'postgres',
        port: 5432
    });
}

module.exports = sequelize;
