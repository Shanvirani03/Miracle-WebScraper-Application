//Configuration file to connect to our database.
const { Pool } = require('pg');
const dotenv = require('dotenv');

dotenv.config();

//Stored sensitive variables in .env file.
const pool = new Pool({
  user: process.env.PG_USER,
  host: process.env.PG_HOST,
  database: process.env.PG_DATABASE,
  password: process.env.PG_PASSWORD,
  port: process.env.PG_PORT,
});

module.exports = {
  query: (text, params) => pool.query(text, params),
};
