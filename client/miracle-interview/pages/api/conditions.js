// Import the database connection module
import db from "./db";

// Handler function for the API endpoint
// Used pagination in queries because there is too much data which exceeds the limit of API calls.
// By default, there will be 1 page, with 10 items per page.
export default async function handler(req, res) {
  const { page = 1, limit = 10 } = req.query;
  const offset = (page - 1) * limit;

  try {
    // Query to fetch medical conditions and their trial counts with pagination
    const result = await db.query(`
      SELECT medical_condition, COUNT(*) AS trial_count
      FROM combined
      GROUP BY medical_condition
      ORDER BY medical_condition
      LIMIT $1 OFFSET $2
    `, [limit, offset]);

    // Query to fetch the total count of distinct medical conditions
    const totalCount = await db.query(`SELECT COUNT(DISTINCT medical_condition) FROM combined`);
    
    // Respond with the queried data and the total count
    res.status(200).json({ data: result.rows, total: totalCount.rows[0].count });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
