/**
 * FROZEN CONTRACT — curriculum navigation data, generated from book_structure_map.json.
 * 10 themes -> 50 lessons; 10 Word Reviews interleaved after their theme's lessons.
 */

export const THEMES = [
  { theme_id: 1, theme_name: 'General Business', lessons: [1, 2, 3, 4, 5], review_id: 1 },
  { theme_id: 2, theme_name: 'Office Issues', lessons: [6, 7, 8, 9, 10], review_id: 2 },
  { theme_id: 3, theme_name: 'Personnel', lessons: [11, 12, 13, 14, 15], review_id: 3 },
  { theme_id: 4, theme_name: 'Purchasing', lessons: [16, 17, 18, 19, 20], review_id: 4 },
  { theme_id: 5, theme_name: 'Financing and Budgeting', lessons: [21, 22, 23, 24, 25], review_id: 5 },
  { theme_id: 6, theme_name: 'Management Issues', lessons: [26, 27, 28, 29, 30], review_id: 6 },
  { theme_id: 7, theme_name: 'Restaurants and Events', lessons: [31, 32, 33, 34, 35], review_id: 7 },
  { theme_id: 8, theme_name: 'Travel', lessons: [36, 37, 38, 39, 40], review_id: 8 },
  { theme_id: 9, theme_name: 'Entertainment', lessons: [41, 42, 43, 44, 45], review_id: 9 },
  { theme_id: 10, theme_name: 'Health', lessons: [46, 47, 48, 49, 50], review_id: 10 },
];

/** lesson_id -> title, taken verbatim from book_structure_map.json. */
export const LESSON_TITLES = {
  1: 'Contracts', 2: 'Marketing', 3: 'Warranties', 4: 'Business Planning', 5: 'Conferences',
  6: 'Computers', 7: 'Office Technology', 8: 'Office Procedures', 9: 'Electronics', 10: 'Correspondence',
  11: 'Job Advertising and Recruiting', 12: 'Applying and Interviewing', 13: 'Hiring and Training',
  14: 'Salaries and Benefits', 15: 'Promotions, Pensions, and Awards',
  16: 'Shopping', 17: 'Ordering Supplies', 18: 'Shipping', 19: 'Invoices', 20: 'Inventory',
  21: 'Banking', 22: 'Accounting', 23: 'Investments', 24: 'Taxes', 25: 'Financial Statements',
  26: 'Property and Departments', 27: 'Board Meetings and Committees', 28: 'Quality Control',
  29: 'Product Development', 30: 'Renting and Leasing',
  31: 'Selecting a Restaurant', 32: 'Eating Out', 33: 'Ordering Lunch',
  34: 'Cooking as a Career', 35: 'Events',
  36: 'General Travel', 37: 'Airlines', 38: 'Trains', 39: 'Hotels', 40: 'Car Rentals',
  41: 'Movies', 42: 'Theater', 43: 'Music', 44: 'Museums', 45: 'Media',
  46: "Doctor's Office", 47: "Dentist's Office", 48: 'Health Insurance',
  49: 'Hospitals', 50: 'Pharmacy',
};

/** review_id -> {theme_name, lessons}. */
export const WORD_REVIEWS = THEMES.map((t) => ({
  review_id: t.review_id,
  theme_name: t.theme_name,
  lessons: t.lessons,
}));

export function lessonTitle(id) {
  return LESSON_TITLES[id] || `Lesson ${id}`;
}

export function themeForLesson(id) {
  return THEMES.find((t) => t.lessons.includes(Number(id))) || null;
}

/** Total number of learnable vocabulary items across the book. */
export const TOTAL_WORDS = 50 * 12;

export default { THEMES, LESSON_TITLES, WORD_REVIEWS, lessonTitle, themeForLesson, TOTAL_WORDS };
