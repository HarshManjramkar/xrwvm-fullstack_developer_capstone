const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

let reviews_data = { reviews: [] };
let dealerships_data = { dealerships: [] };

try {
  const revPath1 = path.join(__dirname, 'data', 'reviews.json');
  const revPath2 = path.join(__dirname, 'reviews.json');
  if (fs.existsSync(revPath1)) {
    reviews_data = JSON.parse(fs.readFileSync(revPath1, 'utf8'));
  } else if (fs.existsSync(revPath2)) {
    reviews_data = JSON.parse(fs.readFileSync(revPath2, 'utf8'));
  }

  const dealPath1 = path.join(__dirname, 'data', 'dealerships.json');
  const dealPath2 = path.join(__dirname, 'dealerships.json');
  if (fs.existsSync(dealPath1)) {
    dealerships_data = JSON.parse(fs.readFileSync(dealPath1, 'utf8'));
  } else if (fs.existsSync(dealPath2)) {
    dealerships_data = JSON.parse(fs.readFileSync(dealPath2, 'utf8'));
  }
} catch (e) {
  console.error("Error reading JSON files:", e);
}

let inMemoryReviews = [...(reviews_data['reviews'] || [])];
let inMemoryDealerships = [...(dealerships_data['dealerships'] || [])];
let isMongoConnected = false;

mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB', serverSelectionTimeoutMS: 2000 })
  .then(() => {
    isMongoConnected = true;
    console.log("Connected to MongoDB");
    Reviews.deleteMany({}).then(() => Reviews.insertMany(inMemoryReviews)).catch(console.error);
    Dealerships.deleteMany({}).then(() => Dealerships.insertMany(inMemoryDealerships)).catch(console.error);
  })
  .catch((err) => {
    console.log("MongoDB not running, using in-memory JSON data store.");
  });

const Reviews = require('./review');
const Dealerships = require('./dealership');

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    if (isMongoConnected) {
      const documents = await Reviews.find();
      return res.json(documents);
    }
    res.json(inMemoryReviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    if (isMongoConnected) {
      const documents = await Reviews.find({ dealership: dealerId });
      return res.json(documents);
    }
    const filtered = inMemoryReviews.filter(r => r.dealership === dealerId);
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    if (isMongoConnected) {
      const documents = await Dealerships.find();
      return res.json(documents);
    }
    res.json(inMemoryDealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const queryState = req.params.state.toLowerCase();
    if (isMongoConnected) {
      const documents = await Dealerships.find({ state: req.params.state });
      return res.json(documents);
    }
    const filtered = inMemoryDealerships.filter(d => 
      (d.state && d.state.toLowerCase() === queryState) ||
      (d.state_name && d.state_name.toLowerCase() === queryState)
    );
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    if (isMongoConnected) {
      const document = await Dealerships.findOne({ id: id });
      return res.json(document);
    }
    const doc = inMemoryDealerships.find(d => d.id === id);
    res.json(doc || {});
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    let data = typeof req.body === 'string' ? JSON.parse(req.body) : JSON.parse(req.body.toString());
    let new_id = (inMemoryReviews.length > 0 ? Math.max(...inMemoryReviews.map(r => r.id || 0)) : 0) + 1;

    const newRev = {
      "id": new_id,
      "name": data['name'],
      "dealership": parseInt(data['dealership']),
      "review": data['review'],
      "purchase": data['purchase'],
      "purchase_date": data['purchase_date'],
      "car_make": data['car_make'],
      "car_model": data['car_model'],
      "car_year": data['car_year'],
    };

    if (isMongoConnected) {
      const review = new Reviews(newRev);
      const savedReview = await review.save();
      return res.json(savedReview);
    }

    inMemoryReviews.push(newRev);
    res.json(newRev);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
