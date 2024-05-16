// Import the database connection module
import db from "./db";

export default async function handler(req, res) {
  // Extract page and limit from query parameters, with default values
  const { page = 1, limit = 10 } = req.query;
  const offset = (page - 1) * limit;

  try {
    // Query to fetch sponsor names and their trial counts with pagination
    const result = await db.query(`
      SELECT sponsor_name, COUNT(*) AS trial_count
      FROM combined
      GROUP BY sponsor_name
      ORDER BY sponsor_name
      LIMIT $1 OFFSET $2
    `, [limit, offset]);

    // Query to fetch the total count of distinct sponsors
    const totalCount = await db.query(`SELECT COUNT(DISTINCT sponsor_name) FROM combined`);
    
    // Respond with the queried data and the total count
    res.status(200).json({ data: result.rows, total: totalCount.rows[0].count });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
