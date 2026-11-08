/**
 * FROZEN CONTRACT — shared data shapes.
 * Mirrors sample_lessons/lesson_01.json exactly.
 * Do NOT change field names; all tabs and the loader depend on these.
 */

/** @typedef {{pos: 'verb'|'noun'|'adjective'|'adverb', word: string, example: string}} WordFamily */
/** @typedef {{en: string, vi: string}} Example */

/**
 * @typedef {Object} WordEntry
 * @property {number} id
 * @property {string} word
 * @property {string} pos
 * @property {string} ipa
 * @property {string} definition_en
 * @property {string} definition_vi
 * @property {string[]} collocations
 * @property {Example[]} examples
 * @property {WordFamily[]} [word_family]  // some OCR outputs put families in a separate array
 */

/** @typedef {{word_bank: string[], passage: string, answers: Record<string,string>}} WordsInContext */

/** @typedef {{question_num:number, options:Record<string,string>, answer?:string, sentence?:string, question?:string}} Question */

/**
 * @typedef {Object} Lesson
 * @property {number} lesson_id
 * @property {string} title
 * @property {number} theme_id
 * @property {string} theme_name
 * @property {string} audio_track
 * @property {string} part1_photo
 * @property {WordEntry[]} words_to_learn
 * @property {WordsInContext} words_in_context
 * @property {Object} [practice]
 * @property {{listening?:{part1?:Object,part2?:Question[],part3?:Question[],part4?:Question[]},reading?:{part5?:Question[],part6?:Object,part7?:Object}}} [practice]
 */

/** Loading states returned by loadLesson(). */
export const LESSON_STATUS = {
  LOADED: 'loaded',
  NOT_EXTRACTED: 'not_extracted',
  ERROR: 'error',
};

/** Vietnamese label shown when lessons_json/lesson_XX.json is absent. */
export const NOT_EXTRACTED_LABEL = 'Chưa trích xuất';

/** Word-family rows always render in this order. */
export const WORD_FAMILY_ORDER = ['verb', 'noun', 'adjective', 'adverb'];

export const WORD_FAMILY_LABEL = {
  verb: 'Verb',
  noun: 'Noun',
  adjective: 'Adj',
  adverb: 'Adv',
};

export default {};
