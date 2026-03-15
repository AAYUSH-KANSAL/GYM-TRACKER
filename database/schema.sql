-- Gym Progress Tracking App Supabase Schema

-- 1. Profiles Table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE NOT NULL PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE NOT NULL,
  name TEXT,
  email TEXT,
  phone TEXT
);

-- 2. Progress Table
CREATE TABLE progress (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE NOT NULL,
  date DATE NOT NULL,
  weight NUMERIC NOT NULL,
  chest NUMERIC,
  waist NUMERIC,
  biceps NUMERIC,
  thigh NUMERIC,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Workouts Table
CREATE TABLE workouts (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE NOT NULL,
  day TEXT NOT NULL,
  exercise TEXT NOT NULL,
  sets INTEGER NOT NULL,
  reps INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Diets Table
CREATE TABLE diets (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE NOT NULL,
  day TEXT NOT NULL,
  meal_type TEXT NOT NULL,
  food_items TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Optional Row Level Security (RLS) policies 
-- Run these if you want to secure the tables to only the authenticated user that owns the rows
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE diets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can insert their own profile." ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Users can view own profile." ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile." ON profiles FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert their own progress." ON progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can view own progress." ON progress FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can manage their own workouts." ON workouts FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage their own diets." ON diets FOR ALL USING (auth.uid() = user_id);
