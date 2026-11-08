# -*- coding: utf-8 -*-
"""
Vocabulary enrichment data for Batch 2 (Lessons 11-20, 119 words).
"""

BATCH_DATA = {
    11: {
        "abundant": {
            "definition_vi": "dồi dào, phong phú, nhiều",
            "examples_vi": [
                "Chuyên viên phân tích máy tính rất vui vì đã chọn một lĩnh vực mà việc làm rất dồi dào.",
                "Nhà tuyển dụng đã ngạc nhiên trước số lượng dồi dào các ứng viên đủ năng lực."
            ],
            "collocations": [
                "abundant supply",
                "abundant opportunities",
                "abundant resources",
                "in abundant quantities"
            ],
            "usage": {
                "structures": [
                    "be abundant in + N (dồi dào/phong phú về cái gì)",
                    "abundant + N (số lượng nhiều/phong phú)"
                ],
                "prepositions": ["in"],
                "collocations": [
                    "abundant supply",
                    "abundant opportunities",
                    "abundant evidence",
                    "abundant resources"
                ],
                "tip": "Thường đứng trước danh từ đếm được số nhiều hoặc danh từ không đếm được (resources, opportunities, supply) để chỉ sự dồi dào."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "abound",
                    "example": "Job opportunities abound in the rapidly growing technology sector.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "abundance",
                    "example": "The region has an abundance of skilled labor for manufacturing.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "abundant",
                    "example": "Natural resources are abundant in this part of the country.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "abundantly",
                    "example": "The director made it abundantly clear that deadlines must be met.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new industrial park offers an _____ of employment opportunities for local residents.",
                "answer": "abundance",
                "base_word": "abundant",
                "pos_hint": "danh từ",
                "vi": "Khu công nghiệp mới mang lại vô số cơ hội việc làm cho cư dân địa phương."
            }
        },
        "accomplishment": {
            "definition_vi": "thành tựu, thành tích, sự hoàn thành",
            "examples_vi": [
                "Sự thành công của công ty được xây dựng dựa trên những thành tựu ban đầu của nó.",
                "Để vinh danh những thành tích của cô ấy, người quản lý đã được thăng chức."
            ],
            "collocations": [
                "major accomplishment",
                "impressive accomplishment",
                "sense of accomplishment",
                "list of accomplishments"
            ],
            "usage": {
                "structures": [
                    "accomplishment in + N/V-ing (thành tựu trong lĩnh vực gì)",
                    "a sense of accomplishment (cảm giác thành tựu)"
                ],
                "prepositions": ["in", "of"],
                "collocations": [
                    "notable accomplishment",
                    "professional accomplishments",
                    "proud of one's accomplishments",
                    "recognize an accomplishment"
                ],
                "tip": "Danh từ đếm được chỉ những thành tích xuất sắc cần liệt kê trong sơ yếu lý lịch (résumé)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "accomplishedly",
                    "example": "She performed the complex negotiation task accomplishedly.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The guest speaker at tonight's banquet is an _____ economist with twenty years of experience.",
                "answer": "accomplished",
                "base_word": "accomplishment",
                "pos_hint": "tính từ",
                "vi": "Diễn giả khách mời tại bữa tiệc tối nay là một nhà kinh tế học tài năng với hai mươi năm kinh nghiệm."
            }
        },
        "bring together": {
            "definition_vi": "tập hợp lại, gắn kết, quy tụ",
            "examples_vi": [
                "Hằng năm, công ty quy tụ các luật sư hàng đầu và những nhân viên mới tuyển dụng cho một buổi đào tạo.",
                "Mục tiêu của chúng tôi trong năm nay là tập hợp được nhóm sáng tạo nhất mà chúng tôi có thể tìm thấy."
            ],
            "collocations": [
                "bring together experts",
                "bring people together",
                "bring together resources",
                "bring teams together"
            ],
            "usage": {
                "structures": [
                    "bring + O + together / bring together + O (tập hợp ai/cái gì lại với nhau)"
                ],
                "prepositions": ["for", "from"],
                "collocations": [
                    "bring together top talent",
                    "bring together diverse perspectives",
                    "bring departments together",
                    "bring buyers and sellers together"
                ],
                "tip": "Cụm động từ thường xuất hiện trong ngữ cảnh hội nghị, đào tạo hoặc dự án liên phòng ban nhằm quy tụ nhân sự."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "bring",
                    "example": "The merger will bring significant benefits to both corporations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "togetherness",
                    "example": "The company retreat fostered a strong sense of togetherness among staff.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "together",
                    "example": "The marketing and sales departments worked closely together on the launch.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The annual trade summit _____ industry leaders from over thirty countries last month.",
                "answer": "brought together",
                "base_word": "bring together",
                "pos_hint": "cụm động từ chia quá khứ đơn",
                "vi": "Hội nghị thượng đỉnh thương mại thường niên đã quy tụ các nhà lãnh đạo ngành từ hơn ba mươi quốc gia vào tháng trước."
            }
        },
        "candidate": {
            "definition_vi": "ứng viên, thí sinh",
            "examples_vi": [
                "Nhà tuyển dụng sẽ phỏng vấn tất cả các ứng viên cho vị trí này.",
                "Chủ tịch công ty chúng tôi là một ứng viên cho Giải thưởng Doanh nghiệp Xuất sắc."
            ],
            "collocations": [
                "qualified candidate",
                "prospective candidate",
                "ideal candidate",
                "candidate for the position"
            ],
            "usage": {
                "structures": [
                    "candidate for + N (ứng viên cho vị trí/giải thưởng gì)",
                    "screen/interview candidates (sàng lọc/phỏng vấn ứng viên)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "strong candidate",
                    "shortlist of candidates",
                    "job candidate",
                    "potential candidate"
                ],
                "tip": "Luôn đi kèm giới từ 'for' khi chỉ vị trí công việc hoặc giải thưởng mà người đó đang ứng tuyển."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "candidacy",
                    "example": "The board of directors unanimously supported her candidacy for chief executive.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "candidate",
                    "example": "Only candidates with at least five years of management experience will be considered.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Mr. Tanaka withdrew his _____ for the vice presidency after accepting an overseas post.",
                "answer": "candidacy",
                "base_word": "candidate",
                "pos_hint": "danh từ chỉ việc ứng cử",
                "vi": "Ông Tanaka đã rút đơn ứng cử chức phó chủ tịch sau khi nhận một vị trí ở nước ngoài."
            }
        },
        "come up with": {
            "definition_vi": "nghĩ ra, đưa ra, tìm ra (ý tưởng, kế hoạch, giải pháp)",
            "examples_vi": [
                "Để doanh nghiệp nhỏ đó thành công, họ cần phải nghĩ ra một chiến lược mới.",
                "Làm thế nào mà nhân viên mới có thể nghĩ ra ý tưởng cắt giảm chi phí đó chỉ sau một tuần làm việc?"
            ],
            "collocations": [
                "come up with an idea",
                "come up with a solution",
                "come up with a plan",
                "come up with the money"
            ],
            "usage": {
                "structures": [
                    "come up with + N (nghĩ ra/đưa ra giải pháp, ý tưởng, kế hoạch)"
                ],
                "prepositions": ["with"],
                "collocations": [
                    "come up with a new strategy",
                    "come up with an alternative",
                    "come up with a proposal",
                    "come up with creative ways"
                ],
                "tip": "Đồng nghĩa với 'devise' hoặc 'propose' trong bài thi TOEIC; tân ngữ theo sau luôn là danh từ chỉ ý tưởng, giải pháp, kế hoạch hoặc kinh phí."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "come",
                    "example": "Good ideas often come from collaborative brainstorming sessions.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "outcome",
                    "example": "Everyone was pleased with the final outcome of the strategy meeting.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "upcoming",
                    "example": "We need to finalize our proposal before the upcoming board meeting.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The engineering team finally _____ an innovative solution to reduce power consumption.",
                "answer": "came up with",
                "base_word": "come up with",
                "pos_hint": "cụm động từ chia quá khứ đơn",
                "vi": "Đội ngũ kỹ sư cuối cùng đã tìm ra một giải pháp sáng tạo nhằm giảm mức tiêu thụ điện năng."
            }
        },
        "commensurate": {
            "definition_vi": "tương xứng, xứng đáng với",
            "examples_vi": [
                "Nhìn chung, mức lương năm đầu tiên sẽ tương xứng với kinh nghiệm và trình độ học vấn.",
                "Như đã đề cập trong bộ tài liệu của bạn, số lượng nhân viên mới được tuyển sẽ tương xứng với số vị trí còn trống tại công ty."
            ],
            "collocations": [
                "commensurate with experience",
                "salary commensurate with qualifications",
                "commensurate with performance",
                "commensurate reward"
            ],
            "usage": {
                "structures": [
                    "be commensurate with + N (tương xứng/tỷ lệ thuận với cái gì)"
                ],
                "prepositions": ["with"],
                "collocations": [
                    "commensurate with experience",
                    "commensurate with qualifications",
                    "pay commensurate with skills",
                    "commensurate responsibility"
                ],
                "tip": "Trong TOEIC Part 5, 'commensurate' gần như luôn đi kèm giới từ 'with' trong các thông báo tuyển dụng nói về lương thưởng."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "commensurateness",
                    "example": "The audit evaluated the commensurateness of executive pay with company performance.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "commensurate",
                    "example": "Starting compensation will be commensurate with the candidate's prior experience.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "commensurately",
                    "example": "As your responsibilities increase, your salary will rise commensurately.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "When the project scope expanded, the consulting fee was increased _____.",
                "answer": "commensurately",
                "base_word": "commensurate",
                "pos_hint": "trạng từ",
                "vi": "Khi phạm vi dự án mở rộng, mức phí tư vấn đã được tăng lên một cách tương xứng."
            }
        },
        "match": {
            "definition_vi": "(n) người/vật phù hợp, sự tương xứng; (v) ghép nối, phù hợp với",
            "examples_vi": [
                "Rất khó để đưa ra quyết định khi cả hai ứng viên dường như đều là sự lựa chọn hoàn toàn phù hợp.",
                "Chuyên gia săn đầu người kết nối các ứng viên đủ năng lực với những vị trí phù hợp."
            ],
            "collocations": [
                "a perfect match",
                "match candidates to positions",
                "closely match",
                "matching funds"
            ],
            "usage": {
                "structures": [
                    "match + A + to/with + B (ghép/kết nối A phù hợp với B)",
                    "be a good/perfect match for + N (rất phù hợp với cái gì)"
                ],
                "prepositions": ["to", "with", "for"],
                "collocations": [
                    "perfect match for the job",
                    "match the description",
                    "match skills with requirements",
                    "matching records"
                ],
                "tip": "Vừa là danh từ (a good match for...) vừa là ngoại động từ (match A with/to B - không đi kèm giới từ ngay sau động từ khi mang nghĩa khớp với cái gì: match the criteria)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "unmatched",
                    "example": "Our firm offers unmatched expertise in international corporate law.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The automated software works by _____ job seekers' skills with current corporate openings.",
                "answer": "matching",
                "base_word": "match",
                "pos_hint": "danh động từ (V-ing)",
                "vi": "Phần mềm tự động hoạt động bằng cách ghép nối kỹ năng của người tìm việc với các vị trí tuyển dụng hiện tại của công ty."
            }
        },
        "profile": {
            "definition_vi": "(n) hồ sơ, bản mô tả đặc điểm/chân dung; (v) phác họa hồ sơ",
            "examples_vi": [
                "Nhà tuyển dụng nói với anh ấy rằng thật không may, anh không phù hợp với hồ sơ tiêu chí công việc.",
                "Khi công việc thay đổi, tiêu chí hồ sơ ứng viên của công ty cũng thay đổi theo."
            ],
            "collocations": [
                "job profile",
                "company profile",
                "high-profile client",
                "fit the profile"
            ],
            "usage": {
                "structures": [
                    "fit/match the profile (phù hợp với hồ sơ/tiêu chí)",
                    "keep a low/high profile (giữ sự kín tiếng / nổi bật)"
                ],
                "prepositions": ["of", "for"],
                "collocations": [
                    "candidate profile",
                    "corporate profile",
                    "customer profile",
                    "raise the company's profile"
                ],
                "tip": "Thường gặp trong cụm 'fit the job profile' (đáp ứng tiêu chí công việc) hoặc 'company profile' (hồ sơ năng lực công ty)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "profiling",
                    "example": "Customer profiling helps the marketing team target advertisements effectively.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The business magazine _____ ten innovative startup founders in its monthly issue.",
                "answer": "profiled",
                "base_word": "profile",
                "pos_hint": "động từ chia quá khứ đơn (V-ed)",
                "vi": "Tạp chí kinh doanh đã giới thiệu chân dung mười nhà sáng lập khởi nghiệp đổi mới sáng tạo trong số ra hàng tháng."
            }
        },
        "qualifications": {
            "definition_vi": "trình độ chuyên môn, năng lực, bằng cấp",
            "examples_vi": [
                "Người tìm việc đã làm công việc tình nguyện sâu rộng và có thể thêm kinh nghiệm này vào danh sách năng lực chuyên môn của mình.",
                "Ứng viên có nhiều bằng cấp và năng lực đến mức công ty đã tạo ra một vị trí mới cho cô ấy."
            ],
            "collocations": [
                "academic qualifications",
                "professional qualifications",
                "meet the qualifications",
                "minimum qualifications"
            ],
            "usage": {
                "structures": [
                    "qualifications for + N (trình độ/điều kiện cho vị trí gì)",
                    "have/possess the qualifications (có đủ năng lực/bằng cấp)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "list of qualifications",
                    "required qualifications",
                    "impressive qualifications",
                    "check an applicant's qualifications"
                ],
                "tip": "Chú ý phân biệt: 'qualified' (tính từ bổ nghĩa cho người: a qualified applicant) và 'qualifications' (danh từ chỉ bằng cấp/tiêu chuẩn)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "unqualified",
                    "example": "Unqualified applicants will be screened out during the initial review.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To _____ for the senior auditor position, candidates must hold a certified accounting license.",
                "answer": "qualify",
                "base_word": "qualifications",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Để đủ điều kiện cho vị trí kiểm toán viên cao cấp, các ứng viên phải có chứng chỉ hành nghề kế toán."
            }
        },
        "recruit": {
            "definition_vi": "(v) tuyển dụng, chiêu mộ; (n) nhân viên mới tuyển",
            "examples_vi": [
                "Khi công ty tư vấn tuyển dụng cô ấy, họ đã đề nghị chi trả chi phí chuyển chỗ ở cho cô.",
                "Những nhân viên mới tuyển đã dành trọn cả ngày để tham gia đào tạo."
            ],
            "collocations": [
                "new recruit",
                "recruit top talent",
                "recruitment agency",
                "campus recruiting"
            ],
            "usage": {
                "structures": [
                    "recruit + sb + for/into + N (tuyển ai vào vị trí/tổ chức nào)",
                    "new recruits (những nhân viên mới tuyển)"
                ],
                "prepositions": ["for", "from", "into"],
                "collocations": [
                    "recruit qualified staff",
                    "recruitment drive",
                    "raw recruit",
                    "actively recruit"
                ],
                "tip": "Danh từ 'recruit' vừa là động từ vừa là danh từ chỉ người (nhân viên mới: new recruits), còn 'recruitment' là danh từ chỉ quá trình tuyển dụng."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "recruited",
                    "example": "Newly recruited engineers must complete a two-week orientation program.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The human resources department launched an aggressive _____ campaign to staff the new branch.",
                "answer": "recruitment",
                "base_word": "recruit",
                "pos_hint": "danh từ chỉ sự tuyển dụng",
                "vi": "Phòng nhân sự đã phát động một chiến dịch tuyển dụng mạnh mẽ để bổ sung nhân sự cho chi nhánh mới."
            }
        },
        "submit": {
            "definition_vi": "nộp, đệ trình",
            "examples_vi": [
                "Hãy nộp sơ yếu lý lịch của bạn cho phòng nhân sự.",
                "Ứng viên đã nộp tất cả giấy tờ của mình một cách chuyên nghiệp và đúng hạn."
            ],
            "collocations": [
                "submit an application",
                "submit a résumé",
                "submit a proposal",
                "submit a report"
            ],
            "usage": {
                "structures": [
                    "submit + sth + to + sb/sth (nộp cái gì cho ai/bộ phận nào)",
                    "submit + sth + for + approval/review (đệ trình cái gì để phê duyệt/xem xét)"
                ],
                "prepositions": ["to", "for", "by"],
                "collocations": [
                    "submit in person",
                    "submit prior to the deadline",
                    "submit an expense report",
                    "electronic submission"
                ],
                "tip": "Từ cực kỳ phổ biến trong TOEIC; lưu ý đi với giới từ 'to' (nộp cho ai) và 'by' (trước hạn chót nào)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "submitted",
                    "example": "All submitted proposals will be evaluated by the selection committee.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The deadline for the _____ of grant applications has been extended until Friday.",
                "answer": "submission",
                "base_word": "submit",
                "pos_hint": "danh từ",
                "vi": "Hạn chót nộp đơn xin tài trợ đã được gia hạn đến thứ Sáu."
            }
        },
        "time-consuming": {
            "definition_vi": "tốn thời gian, mất nhiều thời gian",
            "examples_vi": [
                "Mặc dù tốn nhiều thời gian, tất cả những người tham gia đều cảm thấy buổi tham quan mở rất đáng giá.",
                "Sau năm cuộc phỏng vấn, cô Lopez đã có được công việc, nhưng đó là quy trình tốn thời gian nhất mà cô từng trải qua."
            ],
            "collocations": [
                "time-consuming process",
                "time-consuming task",
                "time-consuming procedure",
                "extremely time-consuming"
            ],
            "usage": {
                "structures": [
                    "be time-consuming to + V (tốn thời gian để làm gì)",
                    "a time-consuming + N (một công việc/quy trình tốn thời gian)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "time-consuming paperwork",
                    "laborious and time-consuming",
                    "time-consuming manual entry",
                    "prove time-consuming"
                ],
                "tip": "Tính từ ghép luôn có đuôi -ing dù bổ nghĩa cho vật/quy trình (không dùng time-consumed)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "consume",
                    "example": "Administrative tasks consume nearly half of the manager's workday.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "consumption",
                    "example": "New automation tools have reduced the consumption of staff time.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "time-consuming",
                    "example": "Verifying each applicant's references manually is a time-consuming task.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Installing the new payroll software will save the accounting staff from _____ manual calculations.",
                "answer": "time-consuming",
                "base_word": "time-consuming",
                "pos_hint": "tính từ ghép",
                "vi": "Việc cài đặt phần mềm tính lương mới sẽ giúp nhân viên kế toán tránh khỏi những phép tính thủ công tốn thời gian."
            }
        }
    },
    12: {
        "ability": {
            "definition_vi": "khả năng, năng lực",
            "examples_vi": [
                "Năng lực của nhà thiết kế thể hiện rất rõ qua hồ sơ năng lực của cô ấy.",
                "Khả năng làm việc cùng người khác là một yêu cầu cốt lõi."
            ],
            "collocations": [
                "ability to work",
                "leadership ability",
                "to the best of one's ability",
                "demonstrate the ability"
            ],
            "usage": {
                "structures": [
                    "ability + to V (khả năng làm gì)",
                    "to the best of one's ability (hết khả năng của ai)"
                ],
                "prepositions": ["to", "in"],
                "collocations": [
                    "proven ability",
                    "exceptional ability",
                    "problem-solving ability",
                    "assess a candidate's ability"
                ],
                "tip": "Sau 'ability' hầu như luôn là động từ nguyên mẫu có 'to' (ability to V)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "enable",
                    "example": "The new training module will enable staff to handle customer inquiries faster.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "ability",
                    "example": "She has the ability to manage multiple complex projects simultaneously.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "able",
                    "example": "Will you be able to attend the orientation session tomorrow morning?",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "ably",
                    "example": "Mr. Kim was ably assisted by a team of junior researchers.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Upgrading our server capacity will _____ the website to process twice as many orders.",
                "answer": "enable",
                "base_word": "ability",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Việc nâng cấp dung lượng máy chủ sẽ giúp trang web xử lý số lượng đơn hàng gấp đôi."
            }
        },
        "apply": {
            "definition_vi": "nộp đơn ứng tuyển; áp dụng",
            "examples_vi": [
                "Sinh viên mới tốt nghiệp đại học đã nộp đơn xin ba công việc và nhận được cả ba lời mời làm việc.",
                "Tất cả những ai quan tâm nên trực tiếp nộp đơn tại bất kỳ văn phòng chi nhánh nào."
            ],
            "collocations": [
                "apply for a job",
                "apply in person",
                "apply online",
                "apply to a company"
            ],
            "usage": {
                "structures": [
                    "apply for + a position/job/grant (nộp đơn xin vị trí/công việc/tài trợ)",
                    "apply to + a company/organization (nộp đơn vào công ty/tổ chức)"
                ],
                "prepositions": ["for", "to", "in"],
                "collocations": [
                    "apply for a transfer",
                    "apply in writing",
                    "apply a discount",
                    "applicable regulations"
                ],
                "tip": "Phân biệt rõ danh từ chỉ người 'applicant' (ứng viên) và danh từ chỉ vật 'application' (đơn xin việc/ứng dụng)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "applicable",
                    "example": "Please fill out all sections of the form that are applicable to your situation.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All _____ for the internship program must submit two letters of recommendation.",
                "answer": "applicants",
                "base_word": "apply",
                "pos_hint": "danh từ chỉ người số nhiều",
                "vi": "Tất cả các ứng viên cho chương trình thực tập phải nộp hai thư giới thiệu."
            }
        },
        "background": {
            "definition_vi": "nền tảng, kinh nghiệm quá khứ, lý lịch",
            "examples_vi": [
                "Nền tảng kinh nghiệm của bạn trong ngành xuất bản chắc chắn là một lợi thế cho công việc này.",
                "Nhà tuyển dụng đã thực hiện việc kiểm tra lý lịch toàn diện trước khi mời anh ấy nhận việc."
            ],
            "collocations": [
                "background check",
                "educational background",
                "professional background",
                "background in finance"
            ],
            "usage": {
                "structures": [
                    "background in + N (nền tảng chuyên môn trong lĩnh vực gì)",
                    "conduct a background check (tiến hành kiểm tra lý lịch)"
                ],
                "prepositions": ["in", "on"],
                "collocations": [
                    "strong background in sales",
                    "diverse background",
                    "technical background",
                    "background information"
                ],
                "tip": "Đi với giới từ 'in' khi nói về nền tảng kinh nghiệm trong một ngành nghề cụ thể (a background in accounting/engineering)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "background",
                    "example": "Her extensive background in hospitality makes her ideal for the hotel manager role.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "groundwork",
                    "example": "The research team laid the groundwork for the new product launch.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Every prospective employee must undergo a thorough _____ check prior to receiving a formal job offer.",
                "answer": "background",
                "base_word": "background",
                "pos_hint": "danh từ ghép bổ nghĩa",
                "vi": "Mỗi nhân viên tiềm năng phải trải qua quá trình kiểm tra lý lịch kỹ lưỡng trước khi nhận được lời mời làm việc chính thức."
            }
        },
        "be ready for": {
            "definition_vi": "sẵn sàng cho, chuẩn bị sẵn cho",
            "examples_vi": [
                "Nhờ sự tìm hiểu kỹ lưỡng của mình, ứng viên cảm thấy cô đã sẵn sàng cho buổi phỏng vấn với giám đốc chương trình.",
                "Nhà tuyển dụng đã không chuẩn bị tinh thần cho những câu hỏi của ứng viên."
            ],
            "collocations": [
                "be ready for the interview",
                "be ready for a challenge",
                "be ready for launch",
                "get ready for work"
            ],
            "usage": {
                "structures": [
                    "be ready for + N (sẵn sàng cho cái gì)",
                    "be ready to + V (sẵn sàng làm gì)"
                ],
                "prepositions": ["for", "to"],
                "collocations": [
                    "ready for occupancy",
                    "ready for distribution",
                    "ready for inspection",
                    "ready for the next step"
                ],
                "tip": "Dùng 'ready for + cụm danh từ' và 'ready to + động từ nguyên mẫu'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "ready",
                    "example": "Warehouse workers are readying the shipment for morning dispatch.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "readiness",
                    "example": "The emergency drill tested the staff's readiness for unexpected power outages.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "ready",
                    "example": "All promotional materials will be ready for printing by Wednesday.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "readily",
                    "example": "Information about employee benefits is readily available on the company intranet.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Replacement parts for this printer model are _____ available at most office supply stores.",
                "answer": "readily",
                "base_word": "be ready for",
                "pos_hint": "trạng từ",
                "vi": "Phụ tùng thay thế cho mẫu máy in này luôn có sẵn một cách dễ dàng tại hầu hết các cửa hàng văn phòng phẩm."
            }
        },
        "call in": {
            "definition_vi": "mời tới, triệu tập; gọi điện báo (nghỉ ốm)",
            "examples_vi": [
                "Cô gái trẻ hào hứng đến mức khi được mời tới phỏng vấn, cô đã kể cho tất cả những người mình quen.",
                "Trưởng phòng nhân sự đã mời tất cả các ứng viên đủ tiêu chuẩn tới tham dự vòng phỏng vấn thứ hai."
            ],
            "collocations": [
                "call in for an interview",
                "call in a specialist",
                "call in sick",
                "call in an expert"
            ],
            "usage": {
                "structures": [
                    "call + sb + in / call in + sb (mời/triệu tập ai đến làm việc hoặc phỏng vấn)",
                    "be called in for + N (được mời đến để làm gì)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "be called in for questioning",
                    "call in outside consultants",
                    "call in technicians",
                    "call in applicants"
                ],
                "tip": "Thường chia ở thể bị động 'be called in for an interview' (được mời đến phỏng vấn) hoặc chủ động 'call in a technician' (gọi kỹ thuật viên đến hỗ trợ)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "call",
                    "example": "Please call the human resources office to confirm your interview time.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "caller",
                    "example": "The receptionist politely asked the caller to hold the line.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "call",
                    "example": "We received several phone calls regarding the advertised vacancy.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Five of the top candidates were _____ for a final panel interview with the executive board.",
                "answer": "called in",
                "base_word": "call in",
                "pos_hint": "cụm động từ ở dạng bị động (V3/ed)",
                "vi": "Năm trong số các ứng viên hàng đầu đã được mời tới tham dự buổi phỏng vấn hội đồng cuối cùng với ban giám đốc."
            }
        },
        "confidence": {
            "definition_vi": "sự tự tin, lòng tin, sự tín nhiệm",
            "examples_vi": [
                "Những ứng viên tốt luôn thể hiện sự tự tin trong suốt buổi phỏng vấn.",
                "Anh ta có quá nhiều sự tự tin và nghĩ rằng công việc đó chắc chắn thuộc về mình."
            ],
            "collocations": [
                "have confidence in",
                "show confidence",
                "consumer confidence",
                "boost confidence"
            ],
            "usage": {
                "structures": [
                    "confidence in + sb/sth (niềm tin/sự tin tưởng vào ai/cái gì)",
                    "with confidence (một cách tự tin)"
                ],
                "prepositions": ["in", "with"],
                "collocations": [
                    "vote of confidence",
                    "inspire confidence",
                    "gain confidence",
                    "strict confidence"
                ],
                "tip": "Lưu ý giới từ 'in' đi sau cả danh từ và tính từ: 'confidence in' và 'confident in/about'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "confide",
                    "example": "Employees should feel comfortable confiding their concerns to the HR counselor.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Ms. Rivera answered the panel's technical questions _____ and impressed all the interviewers.",
                "answer": "confidently",
                "base_word": "confidence",
                "pos_hint": "trạng từ",
                "vi": "Cô Rivera đã trả lời các câu hỏi kỹ thuật của hội đồng một cách tự tin và gây ấn tượng với tất cả những người phỏng vấn."
            }
        },
        "constantly": {
            "definition_vi": "liên tục, luôn luôn, không ngừng",
            "examples_vi": [
                "Công ty luôn liên tục tìm kiếm những nhân viên được đào tạo bài bản.",
                "Martin liên tục kiểm tra tin nhắn của mình để xem có ai gọi điện mời phỏng vấn hay không."
            ],
            "collocations": [
                "constantly changing",
                "constantly looking for",
                "constantly improving",
                "constantly evolving"
            ],
            "usage": {
                "structures": [
                    "constantly + V / be + constantly + V-ing / V3 (liên tục làm gì / được làm gì)"
                ],
                "prepositions": [],
                "collocations": [
                    "constantly updated",
                    "constantly monitored",
                    "constantly seeking",
                    "constantly shifting market"
                ],
                "tip": "Trạng từ tần suất thường đứng giữa trợ động từ 'be/have' và động từ chính (is constantly seeking / has constantly improved)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "constancy",
                    "example": "The constancy of her dedication to quality earned her the annual leadership award.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "constant",
                    "example": "The customer support team is under constant pressure to reduce wait times.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "constantly",
                    "example": "Our software engineers are constantly updating security protocols.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To remain competitive, retail businesses must adapt to _____ changes in consumer preferences.",
                "answer": "constant",
                "base_word": "constantly",
                "pos_hint": "tính từ",
                "vi": "Để duy trì khả năng cạnh tranh, các doanh nghiệp bán lẻ phải thích ứng với những thay đổi liên tục trong thị hiếu người tiêu dùng."
            }
        },
        "expert": {
            "definition_vi": "(n) chuyên gia; (adj) thành thạo, chuyên sâu",
            "examples_vi": [
                "Trưởng bộ phận của chúng tôi là một chuyên gia về tài chính.",
                "Ứng viên đã chứng minh rằng anh ấy là một chuyên gia trong lĩnh vực tiếp thị."
            ],
            "collocations": [
                "expert in marketing",
                "expert advice",
                "industry expert",
                "consult an expert"
            ],
            "usage": {
                "structures": [
                    "an expert in/on/at + N/V-ing (chuyên gia trong lĩnh vực gì)",
                    "expert + N (lời khuyên/ý kiến chuyên môn: expert advice/opinion)"
                ],
                "prepositions": ["in", "on", "at"],
                "collocations": [
                    "leading expert",
                    "financial expert",
                    "expert testimony",
                    "expert guidance"
                ],
                "tip": "Phân biệt danh từ đếm được 'expert' (chuyên gia - cần mạo từ a/an hoặc số nhiều) và danh từ không đếm được 'expertise' (chuyên môn)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "expertly",
                    "example": "The mediator expertly resolved the contract dispute between the two firms.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "We hired an external consulting firm because we lacked the internal _____ to manage the merger.",
                "answer": "expertise",
                "base_word": "expert",
                "pos_hint": "danh từ không đếm được chỉ chuyên môn",
                "vi": "Chúng tôi đã thuê một công ty tư vấn bên ngoài vì chúng tôi thiếu chuyên môn nội bộ để quản lý thương vụ sáp nhập."
            }
        },
        "follow up": {
            "definition_vi": "(v) theo sát, thực hiện bước tiếp theo; (n) hành động tiếp nối",
            "examples_vi": [
                "Hãy luôn theo sát sau buổi phỏng vấn bằng một bức thư cảm ơn.",
                "Như một bước tiếp theo, ứng viên đã gửi cho công ty danh sách những người giới thiệu."
            ],
            "collocations": [
                "follow up on a lead",
                "follow up with a client",
                "follow-up call",
                "as a follow-up"
            ],
            "usage": {
                "structures": [
                    "follow up + with + sb (liên hệ tiếp với ai sau sự việc trước đó)",
                    "follow up + on + sth (theo dõi/xử lý tiếp vấn đề gì)"
                ],
                "prepositions": ["with", "on"],
                "collocations": [
                    "follow-up appointment",
                    "follow-up email",
                    "follow up promptly",
                    "require a follow-up"
                ],
                "tip": "Khi làm động từ thì viết rời (follow up), khi làm danh từ hoặc tính từ ghép đứng trước danh từ thường có gạch nối (a follow-up email)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "follow",
                    "example": "All visitors must follow the safety guidelines while touring the plant.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "follow-up",
                    "example": "The sales representative scheduled a follow-up with the prospective buyer.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "following",
                    "example": "The orientation session will take place on the following Monday.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "After the initial product demonstration, the account manager _____ with each attendee by phone.",
                "answer": "followed up",
                "base_word": "follow up",
                "pos_hint": "cụm động từ chia quá khứ đơn",
                "vi": "Sau buổi giới thiệu sản phẩm ban đầu, quản lý khách hàng đã liên hệ tiếp với từng người tham dự qua điện thoại."
            }
        },
        "hesitant": {
            "definition_vi": "do dự, ngập ngừng, lưỡng lự",
            "examples_vi": [
                "Marla đã do dự về việc đàm phán một mức lương cao hơn.",
                "Sinh viên mới tốt nghiệp đại học đã lưỡng lự trong việc chấp nhận lời mời làm việc đầu tiên của mình."
            ],
            "collocations": [
                "hesitant to accept",
                "hesitant about investing",
                "seem hesitant",
                "understandably hesitant"
            ],
            "usage": {
                "structures": [
                    "be hesitant to + V (do dự khi làm gì)",
                    "be hesitant about + N/V-ing (ngập ngừng/lưỡng lự về việc gì)"
                ],
                "prepositions": ["to", "about"],
                "collocations": [
                    "hesitant to make a commitment",
                    "hesitant about changing jobs",
                    "hesitant response",
                    "remain hesitant"
                ],
                "tip": "Chú ý cấu trúc cố định trong thư tín thương mại: 'Please do not hesitate to contact us' (Đừng ngần ngại liên hệ với chúng tôi)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "hesitantly",
                    "example": "The intern spoke hesitantly when asked to explain the budget error.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Should you require any further assistance, please do not _____ to contact our support desk.",
                "answer": "hesitate",
                "base_word": "hesitant",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Nếu quý khách cần bất kỳ sự hỗ trợ nào thêm, xin đừng ngần ngại liên hệ với bộ phận hỗ trợ của chúng tôi."
            }
        },
        "present": {
            "definition_vi": "trình bày, xuất trình, giới thiệu, trao tặng",
            "examples_vi": [
                "Giám đốc nhân sự trình sơ yếu lý lịch của từng ứng viên lên giám sát viên bộ phận để xem xét.",
                "Ứng viên đã trình bày năng lực chuyên môn của mình tốt đến mức nhà tuyển dụng mời cô nhận việc ngay tại chỗ."
            ],
            "collocations": [
                "present a résumé",
                "present findings",
                "present an award",
                "present credentials"
            ],
            "usage": {
                "structures": [
                    "present + sth + to + sb (trình bày/xuất trình cái gì cho ai)",
                    "present + sb + with + sth (trao tặng cho ai cái gì)"
                ],
                "prepositions": ["to", "with", "at"],
                "collocations": [
                    "present a proposal",
                    "present identification",
                    "present an opportunity",
                    "give a presentation"
                ],
                "tip": "Ngoài nghĩa động từ 'trình bày/trao tặng', 'present' còn là tính từ mang nghĩa 'có mặt' (be present at the meeting)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "presenter",
                    "example": "The keynote presenter shared valuable insights on talent retention.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Ms. Ortiz gave an impressive _____ on market expansion strategies at the annual conference.",
                "answer": "presentation",
                "base_word": "present",
                "pos_hint": "danh từ",
                "vi": "Bà Ortiz đã có một bài thuyết trình ấn tượng về các chiến lược mở rộng thị trường tại hội nghị thường niên."
            }
        },
        "weakly": {
            "definition_vi": "một cách yếu ớt, kém cỏi, mờ nhạt",
            "examples_vi": [
                "Đôi tay cô run rẩy và cô nói chuyện một cách yếu ớt tại buổi phỏng vấn.",
                "Cô ấy viết mờ và yếu đến mức chúng tôi không thể đọc được."
            ],
            "collocations": [
                "speak weakly",
                "smile weakly",
                "respond weakly",
                "perform weakly"
            ],
            "usage": {
                "structures": [
                    "V + weakly (làm việc gì một cách yếu ớt/kém hiệu quả)"
                ],
                "prepositions": [],
                "collocations": [
                    "shake hands weakly",
                    "argue weakly",
                    "weakly correlated",
                    "react weakly"
                ],
                "tip": "Trong ngữ cảnh phỏng vấn TOEIC, danh từ 'strengths and weaknesses' (điểm mạnh và điểm yếu) và động từ 'weaken' xuất hiện rất thường xuyên."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "weaken",
                    "example": "Rising raw material costs could weaken the company's profit margins this quarter.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "During the interview, candidates are often asked to describe their greatest strengths and _____.",
                "answer": "weaknesses",
                "base_word": "weakly",
                "pos_hint": "danh từ số nhiều",
                "vi": "Trong buổi phỏng vấn, các ứng viên thường được yêu cầu mô tả những điểm mạnh và điểm yếu lớn nhất của họ."
            }
        }
    },
    13: {
        "conduct": {
            "definition_vi": "(n) hạnh kiểm, cách cư xử; (v) tiến hành, thực hiện, cư xử",
            "examples_vi": [
                "Cách cư xử của các thực tập sinh trong suốt khóa đào tạo là không thể chấp nhận được.",
                "Các cuộc phỏng vấn đã được tiến hành trong khoảng thời gian ba tuần."
            ],
            "collocations": [
                "conduct an interview",
                "conduct a survey",
                "code of conduct",
                "conduct research"
            ],
            "usage": {
                "structures": [
                    "conduct + a survey/interview/inspection/audit (tiến hành khảo sát/phỏng vấn/kiểm tra/kiểm toán)",
                    "code of conduct (quy tắc ứng xử)"
                ],
                "prepositions": ["by", "over"],
                "collocations": [
                    "conduct business",
                    "conduct an investigation",
                    "professional conduct",
                    "conduct training sessions"
                ],
                "tip": "Một trong những động từ kinh điển nhất của TOEIC, thường đi kèm các danh từ chỉ hoạt động chính thức như 'survey, interview, research, inspection, audit'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "conducive",
                    "example": "A quiet office layout is conducive to higher employee productivity.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "An independent accounting firm was hired to _____ a comprehensive audit of the branch's finances.",
                "answer": "conduct",
                "base_word": "conduct",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Một công ty kế toán độc lập đã được thuê để tiến hành kiểm toán toàn diện tình hình tài chính của chi nhánh."
            }
        },
        "generate": {
            "definition_vi": "tạo ra, phát sinh, mang lại",
            "examples_vi": [
                "Chương trình đào tạo mới đã tạo ra rất nhiều sự quan tâm trong đội ngũ nhân viên.",
                "Ngày hội việc làm tại khuôn viên trường đại học sẽ thu hút sự quan tâm đối với công ty chúng ta."
            ],
            "collocations": [
                "generate interest",
                "generate revenue",
                "generate electricity",
                "generate new leads"
            ],
            "usage": {
                "structures": [
                    "generate + revenue/interest/profits/ideas (tạo ra doanh thu/sự quan tâm/lợi nhuận/ý tưởng)"
                ],
                "prepositions": ["from", "among"],
                "collocations": [
                    "generate income",
                    "generate publicity",
                    "generate enthusiasm",
                    "computer-generated report"
                ],
                "tip": "Thường đi với các tân ngữ trừu tượng trong kinh doanh như 'revenue, profit, interest, publicity, sales'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "generation",
                    "example": "The company is investing heavily in solar power generation.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "generative",
                    "example": "Generative design software has accelerated our prototype development.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new digital advertising campaign _____ over two million dollars in additional sales last quarter.",
                "answer": "generated",
                "base_word": "generate",
                "pos_hint": "động từ chia quá khứ đơn (V-ed)",
                "vi": "Chiến dịch quảng cáo kỹ thuật số mới đã mang lại hơn hai triệu đô la doanh số tăng thêm vào quý trước."
            }
        },
        "hire": {
            "definition_vi": "(n) nhân viên mới được thuê; (v) thuê, tuyển dụng",
            "examples_vi": [
                "Nhân viên mới được tuyển đã hòa nhập rất tốt với các đồng nghiệp của mình.",
                "Cô ấy đã được tuyển dụng sau buổi phỏng vấn thứ ba."
            ],
            "collocations": [
                "new hire",
                "hire additional staff",
                "hiring process",
                "hiring freeze"
            ],
            "usage": {
                "structures": [
                    "hire + sb + as + N (thuê ai làm vị trí gì)",
                    "new hires (những nhân viên mới tuyển)"
                ],
                "prepositions": ["as", "for"],
                "collocations": [
                    "hire a contractor",
                    "hiring manager",
                    "for hire",
                    "hire on a temporary basis"
                ],
                "tip": "Lưu ý trong tiếng Anh thương mại Mỹ, 'new hire' là danh từ đếm được rất phổ biến chỉ 'nhân viên mới vào làm'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "hiring",
                    "example": "The human resources director oversees all hiring for the regional offices.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "hired",
                    "example": "Newly hired technicians must attend a mandatory safety workshop.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Due to budget constraints, the corporation announced a temporary freeze on _____ new personnel.",
                "answer": "hiring",
                "base_word": "hire",
                "pos_hint": "danh động từ (V-ing)",
                "vi": "Do hạn chế về ngân sách, tập đoàn đã thông báo tạm ngừng việc tuyển dụng nhân sự mới."
            }
        },
        "keep up with": {
            "definition_vi": "theo kịp, bắt kịp, nắm bắt kịp",
            "examples_vi": [
                "Các công nhân được thông báo rằng họ phải theo kịp những thay đổi nếu không sẽ rơi vào cảnh mất việc.",
                "Nhân viên được khuyến khích tham gia các khóa học để bắt kịp những sự phát triển mới."
            ],
            "collocations": [
                "keep up with changes",
                "keep up with demand",
                "keep up with technology",
                "keep up with competitors"
            ],
            "usage": {
                "structures": [
                    "keep up with + N (theo kịp/đáp ứng kịp cái gì)"
                ],
                "prepositions": ["with"],
                "collocations": [
                    "keep up with the latest trends",
                    "keep up with market developments",
                    "struggle to keep up with orders",
                    "keep up with industry standards"
                ],
                "tip": "Rất hay xuất hiện trong cụm 'keep up with growing demand' (đáp ứng kịp nhu cầu ngày càng tăng) hoặc 'keep up with technological advances'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "keep",
                    "example": "Please keep all receipts for travel expenses to claim reimbursement.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "upkeep",
                    "example": "The tenant is responsible for the routine upkeep of the leased premises.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "keeper",
                    "example": "The bookkeeper reconciles the company's bank statements every Friday.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The factory hired twenty additional assembly workers in order to _____ the surge in holiday orders.",
                "answer": "keep up with",
                "base_word": "keep up with",
                "pos_hint": "cụm động từ nguyên mẫu",
                "vi": "Nhà máy đã thuê thêm hai mươi công nhân lắp ráp để đáp ứng kịp lượng đơn hàng tăng vọt trong dịp lễ."
            }
        },
        "look up to": {
            "definition_vi": "kính trọng, ngưỡng mộ",
            "examples_vi": [
                "Các nhân viên luôn kính trọng vị giám đốc vì ông đã giành được sự tôn trọng của họ qua nhiều năm.",
                "Có rất ít người trên thế giới này mà tôi ngưỡng mộ nhiều như tôi ngưỡng mộ bạn."
            ],
            "collocations": [
                "look up to a mentor",
                "look up to the director",
                "someone to look up to",
                "widely looked up to"
            ],
            "usage": {
                "structures": [
                    "look up to + sb (ngưỡng mộ/kính trọng ai)"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "look up to senior colleagues",
                    "look up to a leader",
                    "look up to a role model",
                    "greatly look up to"
                ],
                "tip": "Phân biệt các cụm với 'look': 'look up to' (kính trọng), 'look forward to' (mong đợi), 'look into' (điều tra), 'look over' (xem qua)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "look",
                    "example": "Let's look closely at the third-quarter training expenses.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "outlook",
                    "example": "The economic outlook for the upcoming fiscal year remains positive.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "forward-looking",
                    "example": "A forward-looking leadership team invests heavily in employee development.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Junior associates _____ Ms. Kapoor because of her integrity and decades of industry leadership.",
                "answer": "look up to",
                "base_word": "look up to",
                "pos_hint": "cụm động từ hiện tại đơn",
                "vi": "Các nhân viên cấp dưới luôn kính trọng bà Kapoor vì sự chính trực và hàng chục năm dẫn dắt ngành của bà."
            }
        },
        "mentor": {
            "definition_vi": "(n) người hướng dẫn, người cố vấn; (v) cố vấn, dìu dắt",
            "examples_vi": [
                "Người cố vấn đã giúp cô đưa ra một số quyết định về việc kết hợp giữa sự nghiệp và gia đình.",
                "Một vấn đề với nhiều chương trình là những người hướng dẫn không cảm thấy gắn bó với sự tiến bộ của những nhân viên mà họ đang làm việc cùng."
            ],
            "collocations": [
                "assign a mentor",
                "mentoring program",
                "experienced mentor",
                "mentor new recruits"
            ],
            "usage": {
                "structures": [
                    "act/serve as a mentor to + sb (đóng vai trò cố vấn cho ai)",
                    "mentor + sb (hướng dẫn/dìu dắt ai)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "career mentor",
                    "peer mentorship",
                    "trusted mentor",
                    "corporate mentoring"
                ],
                "tip": "Vừa là danh từ chỉ người (mentor) vừa là động từ (mentor junior staff); danh từ chỉ chương trình/vai trò cố vấn là 'mentorship' hoặc 'mentoring'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "mentor",
                    "example": "Senior engineers are encouraged to mentor newly hired graduates.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "mentorship",
                    "example": "The company's formal mentorship program has significantly reduced employee turnover.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "mentee",
                    "example": "Each mentor meets with their mentee twice a month to review career goals.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Under the _____ of the chief architect, the young designer quickly mastered commercial blueprints.",
                "answer": "mentorship",
                "base_word": "mentor",
                "pos_hint": "danh từ chỉ sự hướng dẫn/cố vấn",
                "vi": "Dưới sự dìu dắt của kiến trúc sư trưởng, nhà thiết kế trẻ đã nhanh chóng thành thạo các bản vẽ thương mại."
            }
        },
        "on track": {
            "definition_vi": "đúng tiến độ, đi đúng hướng",
            "examples_vi": [
                "Nếu chúng ta bám sát đúng tiến độ, cuộc họp sẽ kết thúc lúc 9 giờ 30.",
                "Bạn có rất nhiều việc; nếu bạn không thể theo kịp tiến độ, hãy báo cho tôi biết ngay lập tức."
            ],
            "collocations": [
                "stay on track",
                "keep on track",
                "back on track",
                "on track to meet the goal"
            ],
            "usage": {
                "structures": [
                    "be/stay/keep + on track (đúng tiến độ / giữ đúng hướng)",
                    "on track + to V / for N (đang đi đúng hướng để đạt được điều gì)"
                ],
                "prepositions": ["to", "for", "with"],
                "collocations": [
                    "get the project back on track",
                    "remain on track",
                    "well on track",
                    "on track for completion"
                ],
                "tip": "Cụm giới từ đóng vai trò như tính từ sau động từ 'be, stay, remain, keep, get' để chỉ dự án đang đúng lịch trình."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "track",
                    "example": "You can track the status of your shipment online using the confirmation number.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "tracker",
                    "example": "The project manager uses a digital tracker to monitor team milestones.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "tracking",
                    "example": "Automated time tracking has simplified payroll processing.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Despite initial supply delays, the construction project is now _____ for its scheduled October opening.",
                "answer": "on track",
                "base_word": "on track",
                "pos_hint": "cụm tính từ chỉ đúng tiến độ",
                "vi": "Bất chấp sự chậm trễ nguồn cung ban đầu, dự án xây dựng hiện đang đúng tiến độ cho lễ khai trương dự kiến vào tháng Mười."
            }
        },
        "reject": {
            "definition_vi": "(v) từ chối, bác bỏ, loại bỏ; (n) phế phẩm, hàng bị loại",
            "examples_vi": [
                "Chúng tôi bỏ những sản phẩm bị loại vào chiếc hộp này.",
                "Mặc dù ông Lukin đã từ chối lời đề nghị của họ, họ vẫn giữ liên lạc."
            ],
            "collocations": [
                "reject an offer",
                "reject a proposal",
                "factory rejects",
                "rejection letter"
            ],
            "usage": {
                "structures": [
                    "reject + an offer/proposal/application (từ chối lời đề nghị/đề xuất/đơn đăng ký)"
                ],
                "prepositions": ["as", "for"],
                "collocations": [
                    "flatly reject",
                    "reject a claim",
                    "reject defective goods",
                    "fear of rejection"
                ],
                "tip": "Đồng nghĩa với 'turn down' hoặc 'decline'; lưu ý danh từ 'reject' (trọng âm rơi vào âm tiết đầu) có nghĩa là hàng lỗi/phế phẩm."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "rejected",
                    "example": "Rejected applications are kept on file for six months.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The zoning board issued a formal _____ of the developer's request to build a taller structure.",
                "answer": "rejection",
                "base_word": "reject",
                "pos_hint": "danh từ",
                "vi": "Ban quy hoạch đã đưa ra văn bản từ chối chính thức đối với yêu cầu xây dựng công trình cao hơn của chủ đầu tư."
            }
        },
        "set up": {
            "definition_vi": "(v) thiết lập, sắp xếp, thành lập; (adj) đã được chuẩn bị sẵn sàng",
            "examples_vi": [
                "Hãy kiểm tra với người giám sát của bạn để đảm bảo rằng văn phòng của bạn đã được bố trí sẵn sàng trước khi bạn bắt đầu làm việc.",
                "Hãy sắp xếp thời gian và địa điểm cho cuộc họp rồi thông báo cho tất cả những người có liên quan."
            ],
            "collocations": [
                "set up a meeting",
                "set up an account",
                "set up a business",
                "set up equipment"
            ],
            "usage": {
                "structures": [
                    "set up + a meeting/appointment/company (sắp xếp cuộc họp / thành lập công ty)",
                    "be set up (đã được lắp đặt/chuẩn bị xong)"
                ],
                "prepositions": ["for", "with"],
                "collocations": [
                    "set up a booth",
                    "set up a committee",
                    "set up a workstation",
                    "initial setup"
                ],
                "tip": "Quá khứ và quá khứ phân từ giữ nguyên là 'set up'; khi viết liền 'setup' (danh từ) có nghĩa là cách bố trí hoặc quá trình cài đặt."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "set",
                    "example": "The executive committee set ambitious sales targets for the fourth quarter.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "setup",
                    "example": "The technician completed the setup of the new conference room projector.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "setting",
                    "example": "Please adjust the printer settings before printing the brochures.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Our IT specialists have already _____ the audiovisual equipment in the main auditorium.",
                "answer": "set up",
                "base_word": "set up",
                "pos_hint": "cụm động từ chia quá khứ phân từ (V3)",
                "vi": "Các chuyên gia CNTT của chúng tôi đã lắp đặt xong thiết bị nghe nhìn tại hội trường chính."
            }
        },
        "success": {
            "definition_vi": "sự thành công, thắng lợi",
            "examples_vi": [
                "Sự thành công của vị giám đốc đến sau nhiều năm tuyển dụng đúng người vào đúng thời điểm.",
                "Khi người quản lý giành được giải thưởng, ông đã quy sự thành công của mình là nhờ các đồng nghiệp."
            ],
            "collocations": [
                "achieve success",
                "attribute success to",
                "resounding success",
                "key to success"
            ],
            "usage": {
                "structures": [
                    "succeed in + V-ing/N (thành công trong việc gì)",
                    "be a great/huge success (là một thành công lớn)"
                ],
                "prepositions": ["in", "with"],
                "collocations": [
                    "commercial success",
                    "long-term success",
                    "measure of success",
                    "prove a success"
                ],
                "tip": "Cẩn thận bẫy từ loại kinh điển trong TOEIC: 'succeed' là động từ, 'success' là danh từ, 'successful' là tính từ, còn 'successive' là tính từ mang nghĩa 'liên tiếp'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "successfully",
                    "example": "All trainees successfully completed the certification exam.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The software migration was _____ completed over the weekend without any data loss.",
                "answer": "successfully",
                "base_word": "success",
                "pos_hint": "trạng từ",
                "vi": "Quá trình chuyển đổi phần mềm đã được hoàn tất thành công vào dịp cuối tuần mà không bị mất dữ liệu nào."
            }
        },
        "training": {
            "definition_vi": "sự đào tạo, việc huấn luyện",
            "examples_vi": [
                "Nhân viên mới được đào tạo tốt đến mức chỉ trong vòng một tuần, cô đã làm việc năng suất như những công nhân khác.",
                "Khóa đào tạo được thiết kế để chuẩn bị cho tất cả công nhân, cả mới lẫn cũ, trước những thay đổi mà công ty sẽ đối mặt."
            ],
            "collocations": [
                "training session",
                "on-the-job training",
                "undergo training",
                "training manual"
            ],
            "usage": {
                "structures": [
                    "training in + N (đào tạo về lĩnh vực gì)",
                    "provide/receive training (cung cấp/nhận sự đào tạo)"
                ],
                "prepositions": ["in", "for", "on"],
                "collocations": [
                    "intensive training program",
                    "safety training",
                    "staff training",
                    "vocational training"
                ],
                "tip": "Phân biệt rõ cặp danh từ chỉ người: 'trainer' (người hướng dẫn/đào tạo) và 'trainee' (người được đào tạo/thực tập sinh)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "trained",
                    "example": "Our service center is staffed by highly trained mechanics.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Every _____ is required to shadow a senior customer service representative for two weeks.",
                "answer": "trainee",
                "base_word": "training",
                "pos_hint": "danh từ chỉ người học việc/thực tập sinh",
                "vi": "Mỗi nhân viên tập sự được yêu cầu theo học hỏi một nhân viên chăm sóc khách hàng cấp cao trong hai tuần."
            }
        },
        "update": {
            "definition_vi": "(v) cập nhật; (n) bản cập nhật, thông tin mới nhất",
            "examples_vi": [
                "Chuyên viên nhân sự đã cập nhật cho các nhân viên về những thay đổi nhân sự mới nhất.",
                "Bản cập nhật mới nhất của chúng tôi cho thấy tình hình kinh doanh đã giảm 15 phần trăm."
            ],
            "collocations": [
                "update the employees on",
                "latest update",
                "status update",
                "software update"
            ],
            "usage": {
                "structures": [
                    "update + sb + on + sth (cập nhật cho ai về thông tin gì)",
                    "an update on + N (thông tin cập nhật về cái gì)"
                ],
                "prepositions": ["on"],
                "collocations": [
                    "periodic updates",
                    "update contact information",
                    "provide an update",
                    "updated version"
                ],
                "tip": "Khi mang nghĩa 'cập nhật thông tin cho ai về việc gì', luôn dùng cấu trúc 'update somebody ON something'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "update",
                    "example": "Please update your emergency contact details on the employee portal.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "update",
                    "example": "The project director gives a brief progress update every Monday morning.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "updated",
                    "example": "An updated schedule of workshops has been posted in the break room.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All staff members will receive an _____ copy of the employee handbook next week.",
                "answer": "updated",
                "base_word": "update",
                "pos_hint": "tính từ (V-ed)",
                "vi": "Tất cả nhân viên sẽ nhận được bản sao đã cập nhật của cuốn sổ tay nhân viên vào tuần tới."
            }
        }
    },
    14: {
        "basis": {
            "definition_vi": "nền tảng, cơ sở; định kỳ",
            "examples_vi": [
                "Người quản lý không có bất kỳ cơ sở nào để sa thải nhân viên đó.",
                "Trên cơ sở mười năm gắn bó trung thành với công ty này, tôi cảm thấy mình xứng đáng có ba tuần nghỉ phép."
            ],
            "collocations": [
                "on the basis of",
                "on a regular basis",
                "on a daily basis",
                "on a temporary basis"
            ],
            "usage": {
                "structures": [
                    "on the basis of + N (dựa trên cơ sở cái gì)",
                    "on a + adj (daily/weekly/regular/temporary) + basis (theo định kỳ hàng ngày/hàng tuần/thường xuyên/tạm thời)"
                ],
                "prepositions": ["on", "of", "for"],
                "collocations": [
                    "form the basis of",
                    "on a first-come, first-served basis",
                    "on a voluntary basis",
                    "legal basis"
                ],
                "tip": "Cụm 'on a [adj] basis' (on a regular/daily/monthly basis) là một trong những cụm cố định xuất hiện nhiều nhất trong đề thi TOEIC Part 5."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "basic",
                    "example": "All new hires must complete a basic accounting course.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "basically",
                    "example": "The two benefit packages are basically identical in coverage.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Performance bonuses are _____ primarily on individual sales figures and customer feedback.",
                "answer": "based",
                "base_word": "basis",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed) ở câu bị động",
                "vi": "Tiền thưởng hiệu suất được tính dựa chủ yếu vào doanh số bán hàng cá nhân và phản hồi của khách hàng."
            }
        },
        "be aware of": {
            "definition_vi": "nhận thức được, biết về, nắm được",
            "examples_vi": [
                "Nhân viên mới không biết về quan điểm của công ty đối với việc làm thêm công việc thứ hai.",
                "Bạn có nắm được lịch sử làm việc trước đây của nhân viên mới không?"
            ],
            "collocations": [
                "be fully aware of",
                "make employees aware of",
                "become aware of",
                "aware of the policy"
            ],
            "usage": {
                "structures": [
                    "be aware of + N/V-ing (biết/nhận thức về điều gì)",
                    "be aware that + S + V (biết rằng...)"
                ],
                "prepositions": ["of"],
                "collocations": [
                    "well aware of the risks",
                    "acutely aware of",
                    "raise awareness of",
                    "public awareness"
                ],
                "tip": "Nếu sau chỗ trống là giới từ 'of' + cụm danh từ, hãy chọn tính từ 'aware' (be aware of)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "awareness",
                    "example": "The campaign aims to increase employee awareness of cybersecurity threats.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "aware",
                    "example": "Please ensure that all team members are aware of the revised safety rules.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "unaware",
                    "example": "Several commuters were unaware of the schedule change.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The workshop was organized to promote greater _____ of workplace wellness programs.",
                "answer": "awareness",
                "base_word": "be aware of",
                "pos_hint": "danh từ",
                "vi": "Buổi hội thảo được tổ chức nhằm nâng cao nhận thức sâu rộng hơn về các chương trình chăm sóc sức khỏe tại nơi làm việc."
            }
        },
        "benefit": {
            "definition_vi": "(n) phúc lợi, lợi ích; (v) hưởng lợi, mang lại lợi ích",
            "examples_vi": [
                "Mặc dù chuyên viên phân tích kiếm được mức lương cao hơn ở công việc mới, chế độ phúc lợi của anh ấy ở công việc trước lại tốt hơn.",
                "Tất cả chúng ta đều hưởng lợi từ chính sách đánh giá định kỳ nửa năm một lần của công ty."
            ],
            "collocations": [
                "employee benefits",
                "fringe benefits",
                "benefit from",
                "mutually beneficial"
            ],
            "usage": {
                "structures": [
                    "benefit from + N (hưởng lợi từ cái gì - nội động từ)",
                    "be beneficial to + sb/sth (có lợi cho ai/cái gì)"
                ],
                "prepositions": ["from", "to", "of"],
                "collocations": [
                    "comprehensive benefits package",
                    "retirement benefits",
                    "health-care benefits",
                    "reap the benefits"
                ],
                "tip": "Khi mang nghĩa 'chế độ đãi ngộ/phúc lợi nhân viên', danh từ luôn dùng ở dạng số nhiều 'benefits' (benefits package, fringe benefits)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "beneficiary",
                    "example": "Please name a primary beneficiary on your life insurance enrollment form.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "beneficially",
                    "example": "The new flexible schedule has beneficially impacted staff morale.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Establishing a partnership with the local university will be mutually _____ to both institutions.",
                "answer": "beneficial",
                "base_word": "benefit",
                "pos_hint": "tính từ",
                "vi": "Việc thiết lập quan hệ đối tác với trường đại học địa phương sẽ mang lại lợi ích chung cho cả hai tổ chức."
            }
        },
        "compensate": {
            "definition_vi": "đền bù, bồi thường, trả thù lao",
            "examples_vi": [
                "Công ty trả thù lao làm thêm giờ cho nhân viên bằng cách trả gấp đôi cho những giờ làm thêm.",
                "Công ty sẽ bồi hoàn cho nhân viên bất kỳ khoản chi phí đi lại nào."
            ],
            "collocations": [
                "compensate for overtime",
                "compensate employees",
                "financial compensation",
                "workers' compensation"
            ],
            "usage": {
                "structures": [
                    "compensate + sb + for + sth (trả thù lao / bồi thường cho ai vì cái gì)",
                    "compensate for + sth (bù đắp cho cái gì)"
                ],
                "prepositions": ["for", "with"],
                "collocations": [
                    "adequately compensated",
                    "compensation package",
                    "seek compensation for damages",
                    "compensatory time off"
                ],
                "tip": "Luôn đi kèm giới từ 'for' khi chỉ lý do được trả công hoặc tổn thất được đền bù (compensate sb for sth)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "compensated",
                    "example": "Sales representatives are generously compensated for exceeding their quotas.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The airline offered hotel vouchers as _____ for the overnight flight cancellation.",
                "answer": "compensation",
                "base_word": "compensate",
                "pos_hint": "danh từ",
                "vi": "Hãng hàng không đã cung cấp phiếu nghỉ khách sạn như khoản đền bù cho việc hủy chuyến bay qua đêm."
            }
        },
        "delicately": {
            "definition_vi": "một cách khéo léo, tế nhị, nhẹ nhàng",
            "examples_vi": [
                "Ban lãnh đạo cấp cao đang xử lý các cuộc đàm phán hợp đồng này một cách khéo léo.",
                "Người quản lý đã tế nhị hỏi thăm về tình hình sức khỏe của khách hàng."
            ],
            "collocations": [
                "handle delicately",
                "negotiate delicately",
                "worded delicately",
                "delicately balanced"
            ],
            "usage": {
                "structures": [
                    "handle/treat/approach + sth + delicately (xử lý việc gì một cách tế nhị/khéo léo)"
                ],
                "prepositions": [],
                "collocations": [
                    "delicately phrased",
                    "delicate negotiations",
                    "delicate matter",
                    "move delicately"
                ],
                "tip": "Thường bổ nghĩa cho các động từ như 'handle, negotiate, phrase, ask' khi nói về các vấn đề nhạy cảm trong công sở."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "delicacy",
                    "example": "Personnel disputes must be handled with great tact and delicacy.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "delicate",
                    "example": "Salary restructuring is a delicate issue that requires careful planning.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "delicately",
                    "example": "The mediator delicately guided both parties toward a compromise.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Because the merger talks are at a _____ stage, executives have declined to comment publicly.",
                "answer": "delicate",
                "base_word": "delicately",
                "pos_hint": "tính từ",
                "vi": "Vì các cuộc đàm phán sáp nhập đang ở giai đoạn nhạy cảm, các giám đốc điều hành đã từ chối bình luận công khai."
            }
        },
        "eligible": {
            "definition_vi": "đủ tư cách, đủ điều kiện hưởng",
            "examples_vi": [
                "Một số nhân viên có thể đủ điều kiện tham gia chương trình hoàn trả học phí.",
                "Tôi không hiểu tại sao mình lại không đủ điều kiện khi tôi đã làm việc cho công ty hơn một năm."
            ],
            "collocations": [
                "eligible for promotion",
                "eligible for benefits",
                "eligible to participate",
                "eligible employees"
            ],
            "usage": {
                "structures": [
                    "be eligible for + N (đủ điều kiện nhận/tham gia cái gì)",
                    "be eligible to + V (đủ điều kiện làm gì)"
                ],
                "prepositions": ["for", "to"],
                "collocations": [
                    "eligible for a refund",
                    "eligible for overtime pay",
                    "eligible voters",
                    "determine eligibility"
                ],
                "tip": "Điểm ngữ pháp trọng tâm TOEIC: 'eligible' đi với 'for + N' hoặc 'to + V', thường dùng cho quyền lợi, bảo hiểm, thăng chức hoặc hoàn tiền."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "eligibility",
                    "example": "Please review the eligibility criteria before submitting your grant application.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "eligible",
                    "example": "Full-time staff become eligible for dental coverage after ninety days.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "ineligible",
                    "example": "Part-time contractors are ineligible for the company pension plan.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "eligibly",
                    "example": "All eligibly enrolled members will receive their membership cards by mail.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The human resources clerk verified the employee's _____ for parental leave benefits.",
                "answer": "eligibility",
                "base_word": "eligible",
                "pos_hint": "danh từ",
                "vi": "Nhân viên phòng nhân sự đã xác minh việc đủ điều kiện hưởng chế độ nghỉ phép chăm con của nhân viên đó."
            }
        },
        "flexibly": {
            "definition_vi": "một cách linh hoạt, mềm dẻo",
            "examples_vi": [
                "Quản lý của tôi suy nghĩ rất linh hoạt, giúp cô ấy giải quyết được nhiều vấn đề hóc búa.",
                "Chúng ta cần phản ứng một cách linh hoạt nếu muốn giữ chân khách hàng trong thị trường cạnh tranh này."
            ],
            "collocations": [
                "respond flexibly",
                "work flexibly",
                "think flexibly",
                "adapt flexibly"
            ],
            "usage": {
                "structures": [
                    "V + flexibly (làm việc/ứng phó một cách linh hoạt)"
                ],
                "prepositions": [],
                "collocations": [
                    "flexible working hours",
                    "workplace flexibility",
                    "manage schedules flexibly",
                    "flexible benefits plan"
                ],
                "tip": "Họ từ 'flexible / flexibility / flexibly' xuất hiện dày đặc trong các bài đọc về giờ làm việc linh hoạt (flexible hours / flextime)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "flex",
                    "example": "Employees can flex their start and end times with supervisor approval.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Many job seekers prioritize schedule _____ when evaluating employment offers.",
                "answer": "flexibility",
                "base_word": "flexibly",
                "pos_hint": "danh từ",
                "vi": "Nhiều người tìm việc ưu tiên sự linh hoạt về lịch trình khi đánh giá các lời mời làm việc."
            }
        },
        "negotiate": {
            "definition_vi": "đàm phán, thương lượng",
            "examples_vi": [
                "Bạn phải biết mình muốn gì và có thể chấp nhận mức nào khi đàm phán tiền lương.",
                "Chuyên viên cộng tác rất mong chờ đến ngày cô có thể tự đàm phán các hợp đồng của riêng mình."
            ],
            "collocations": [
                "negotiate a contract",
                "negotiate a salary",
                "negotiate with suppliers",
                "enter into negotiations"
            ],
            "usage": {
                "structures": [
                    "negotiate + sth (a contract/salary/settlement) (đàm phán cái gì)",
                    "negotiate with + sb + for/over + sth (đàm phán với ai về cái gì)"
                ],
                "prepositions": ["with", "for", "over"],
                "collocations": [
                    "under negotiation",
                    "negotiate favorable terms",
                    "skilled negotiator",
                    "negotiating table"
                ],
                "tip": "Chú ý cụm cố định 'under negotiation' (đang trong quá trình đàm phán) và tính từ 'negotiable' (có thể thương lượng được)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "negotiable",
                    "example": "The starting salary for this executive role is negotiable based on experience.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "After weeks of intense _____, management and the labor union reached a three-year agreement.",
                "answer": "negotiations",
                "base_word": "negotiate",
                "pos_hint": "danh từ số nhiều",
                "vi": "Sau nhiều tuần đàm phán căng thẳng, ban giám đốc và công đoàn lao động đã đạt được một thỏa thuận kéo dài ba năm."
            }
        },
        "raise": {
            "definition_vi": "(n) sự tăng lương; (v) nâng lên, tăng lên, quyên góp, nêu lên",
            "examples_vi": [
                "Với khoản tăng lương của mình, ông Drvoshanov đã có đủ khả năng mua một chiếc ô tô mới.",
                "Chúng ta cần nâng cao tiêu chuẩn về sự đúng giờ."
            ],
            "collocations": [
                "get a pay raise",
                "raise standards",
                "raise funds",
                "raise a question"
            ],
            "usage": {
                "structures": [
                    "raise + O (ngoại động từ: tăng/nâng cái gì lên)",
                    "ask for / receive a raise (xin / nhận khoản tăng lương)"
                ],
                "prepositions": ["by", "to"],
                "collocations": [
                    "annual salary raise",
                    "raise prices",
                    "raise awareness",
                    "raise capital"
                ],
                "tip": "Phân biệt 'raise' (ngoại động từ: luôn có tân ngữ phía sau, VD: raise prices/salaries) và 'rise' (nội động từ: không có tân ngữ, VD: prices rise)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "raise",
                    "example": "The board voted to raise the minimum hourly wage across all stores.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "raise",
                    "example": "She received a five percent merit raise after her annual evaluation.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "raised",
                    "example": "The raised platform in the conference hall improves visibility for attendees.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The charity banquet succeeded in _____ over fifty thousand dollars for the local hospital.",
                "answer": "raising",
                "base_word": "raise",
                "pos_hint": "danh động từ (V-ing)",
                "vi": "Bữa tiệc từ thiện đã thành công trong việc quyên góp hơn năm mươi nghìn đô la cho bệnh viện địa phương."
            }
        },
        "retire": {
            "definition_vi": "nghỉ hưu, về hưu",
            "examples_vi": [
                "Bà đã nghỉ hưu ở tuổi 64 nhưng vẫn tiếp tục tham gia rất tích cực vào công việc tình nguyện.",
                "Nhiều người mong muốn trúng xổ số và nghỉ hưu."
            ],
            "collocations": [
                "retire from the company",
                "early retirement",
                "retirement plan",
                "retirement age"
            ],
            "usage": {
                "structures": [
                    "retire from + N (nghỉ hưu rời khỏi công ty/vị trí nào)",
                    "retire at the age of... (nghỉ hưu ở tuổi...)"
                ],
                "prepositions": ["from", "at", "on"],
                "collocations": [
                    "mandatory retirement",
                    "retirement fund",
                    "retirement party",
                    "retired executive"
                ],
                "tip": "Danh từ 'retirement' rất hay đứng trước danh từ khác tạo thành danh từ ghép: 'retirement plan/fund/party/age/benefits'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "retiree",
                    "example": "The company hosts an annual luncheon for all former employees and retirees.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "We are holding a farewell reception on Friday to honor Mr. Jenkins upon his _____ after thirty years of service.",
                "answer": "retirement",
                "base_word": "retire",
                "pos_hint": "danh từ",
                "vi": "Chúng tôi sẽ tổ chức một buổi tiệc chia tay vào thứ Sáu để vinh danh ông Jenkins nhân dịp ông nghỉ hưu sau ba mươi năm cống hiến."
            }
        },
        "vested": {
            "definition_vi": "được trao quyền hưởng trọn vẹn (quỹ hưu trí/cổ phần); gắn liền quyền lợi",
            "examples_vi": [
                "Ngay vào ngày bà Weng đủ điều kiện hưởng trọn vẹn quỹ hưu trí, bà đã nộp đơn xin nghỉ việc báo trước hai tuần.",
                "Công ty có quyền lợi gắn liền mật thiết với sự hạnh phúc của người lao động."
            ],
            "collocations": [
                "fully vested",
                "vested in the retirement plan",
                "have a vested interest in",
                "vested rights"
            ],
            "usage": {
                "structures": [
                    "become (fully) vested in + N (đủ thâm niên để hưởng trọn quyền lợi trong quỹ hưu trí/cổ phiếu)",
                    "have a vested interest in + N (có lợi ích gắn liền với cái gì)"
                ],
                "prepositions": ["in"],
                "collocations": [
                    "vested pension benefits",
                    "vested shares",
                    "vesting period",
                    "vested interest"
                ],
                "tip": "Nhớ 2 cụm cố định trong TOEIC: 'fully vested in the pension/retirement plan' và 'have a vested interest in'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "vest",
                    "example": "Stock options granted to employees vest over a four-year period.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "vesting",
                    "example": "The employee handbook explains the five-year vesting schedule for matching contributions.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "vested",
                    "example": "Local businesses have a vested interest in improving public transportation.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Employees become fully _____ in the company-sponsored pension fund after five years of continuous employment.",
                "answer": "vested",
                "base_word": "vested",
                "pos_hint": "tính từ (V-ed)",
                "vi": "Nhân viên sẽ có toàn quyền hưởng quỹ hưu trí do công ty tài trợ sau năm năm làm việc liên tục."
            }
        },
        "wage": {
            "definition_vi": "tiền công, tiền lương (thường trả theo giờ hoặc tuần)",
            "examples_vi": [
                "Mức lương theo giờ đã tăng 20 phần trăm trong hai năm qua.",
                "Thực tập sinh dành hơn một nửa số tiền lương của mình để trả tiền thuê nhà."
            ],
            "collocations": [
                "hourly wage",
                "minimum wage",
                "living wage",
                "wage increase"
            ],
            "usage": {
                "structures": [
                    "hourly/minimum/daily + wage(s) (mức lương theo giờ / tối thiểu / theo ngày)",
                    "earn a good wage (kiếm được mức lương khá)"
                ],
                "prepositions": ["of", "for"],
                "collocations": [
                    "wage negotiations",
                    "wage freeze",
                    "competitive wages",
                    "fair wages"
                ],
                "tip": "Phân biệt: 'wage(s)' thường là tiền công trả theo giờ/tuần (hourly wages), còn 'salary' là lương cố định trả theo tháng/năm."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "wage",
                    "example": "The state legislature approved an increase in the minimum wage.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "wages",
                    "example": "Unclaimed wages may be collected at the payroll office on Friday.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Factory workers negotiated higher hourly _____ in their new collective bargaining agreement.",
                "answer": "wages",
                "base_word": "wage",
                "pos_hint": "danh từ số nhiều",
                "vi": "Các công nhân nhà máy đã đàm phán mức tiền công theo giờ cao hơn trong thỏa ước lao động tập thể mới của họ."
            }
        }
    },
    15: {
        "achievement": {
            "definition_vi": "thành tựu, thành tích đạt được",
            "examples_vi": [
                "Những thành tích chính của bạn sẽ được liệt kê trong hồ sơ nhân sự.",
                "Những thành tựu của Joseph trong bộ phận Nghiên cứu & Phát triển (R&D) sẽ đi vào lịch sử công ty."
            ],
            "collocations": [
                "outstanding achievement",
                "lifetime achievement award",
                "academic achievement",
                "recognize an achievement"
            ],
            "usage": {
                "structures": [
                    "achievement in + N (thành tựu trong lĩnh vực gì)",
                    "achieve + a goal/objective/success (đạt được mục tiêu/thành công)"
                ],
                "prepositions": ["in", "of"],
                "collocations": [
                    "remarkable achievement",
                    "crowning achievement",
                    "sense of achievement",
                    "high achiever"
                ],
                "tip": "Động từ 'achieve' luôn đi với các tân ngữ chỉ mục tiêu hoặc kết quả tích cực (achieve goals, targets, objectives, success)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "achievable",
                    "example": "Managers should set realistic and achievable quarterly targets for their teams.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "By streamlining the assembly line, the plant manager _____ a twenty percent reduction in operating costs.",
                "answer": "achieved",
                "base_word": "achievement",
                "pos_hint": "động từ chia quá khứ đơn (V-ed)",
                "vi": "Bằng cách tinh gọn dây chuyền lắp ráp, giám đốc nhà máy đã đạt được mức giảm hai mươi phần trăm chi phí vận hành."
            }
        },
        "contribute": {
            "definition_vi": "đóng góp, góp phần, quyên góp",
            "examples_vi": [
                "Hãy chắc chắn rằng sếp của bạn biết về công sức bạn đã đóng góp cho dự án.",
                "Tất cả nhân viên được yêu cầu đóng góp vài phút thời gian rảnh của mình để dọn dẹp văn phòng."
            ],
            "collocations": [
                "contribute to the project",
                "contribute to a pension fund",
                "make a contribution",
                "valuable contributor"
            ],
            "usage": {
                "structures": [
                    "contribute + (sth) + to + N/V-ing (đóng góp cái gì vào việc gì / góp phần dẫn đến việc gì)",
                    "make a contribution to + N (có sự đóng góp cho cái gì)"
                ],
                "prepositions": ["to", "toward"],
                "collocations": [
                    "contribute significantly to",
                    "charitable contribution",
                    "matching contribution",
                    "contribute ideas"
                ],
                "tip": "Giới từ 'to' đi sau 'contribute' và 'contribution' là giới từ (không phải to-infinitive), nên theo sau nó phải là danh từ hoặc V-ing (contribute to improving...)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "contributory",
                    "example": "All full-time staff are enrolled in a contributory pension scheme.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Dr. Lin received a plaque in recognition of her outstanding _____ to medical research.",
                "answer": "contributions",
                "base_word": "contribute",
                "pos_hint": "danh từ số nhiều",
                "vi": "Tiến sĩ Lin đã nhận được tấm bảng vinh danh nhằm ghi nhận những đóng góp xuất sắc của bà cho nghiên cứu y học."
            }
        },
        "look forward to": {
            "definition_vi": "mong đợi, trông mong, háo hức chờ đón",
            "examples_vi": [
                "Giám đốc khu vực đang rất mong chờ được chuyển sang văn phòng mới rộng hơn.",
                "Chúng tôi rất mong được gặp bạn tại cuộc họp tiếp theo."
            ],
            "collocations": [
                "look forward to hearing from you",
                "look forward to working with you",
                "look forward to meeting you",
                "look forward to the event"
            ],
            "usage": {
                "structures": [
                    "look forward to + V-ing / N (mong đợi làm gì / điều gì)"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "look forward to seeing you",
                    "eagerly look forward to",
                    "look forward to a productive partnership",
                    "look forward to your reply"
                ],
                "tip": "Bẫy ngữ pháp kinh điển nhất trong TOEIC Part 5 & 6: chữ 'to' trong 'look forward to' là giới từ, nên động từ theo sau BẮT BUỘC phải chia dạng V-ing!"
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "look",
                    "example": "We look to expand our regional presence over the next two years.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "forward",
                    "example": "The board approved a bold forward plan for international growth.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "forward",
                    "example": "We are moving forward with the construction of the new warehouse.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "We look forward to _____ your delegation at our Tokyo headquarters next month.",
                "answer": "welcoming",
                "base_word": "look forward to",
                "pos_hint": "danh động từ (V-ing) sau look forward to",
                "vi": "Chúng tôi rất mong được chào đón phái đoàn của quý vị tại trụ sở Tokyo của chúng tôi vào tháng tới."
            }
        },
        "look to": {
            "definition_vi": "trông cậy vào, dựa vào, kỳ vọng vào",
            "examples_vi": [
                "Các công nhân luôn trông cậy vào ông ấy để giải quyết những bất đồng của họ.",
                "Đội ngũ nhân viên đang trông cậy vào người giám sát của họ để có sự hướng dẫn và định hướng."
            ],
            "collocations": [
                "look to a supervisor for guidance",
                "look to the future",
                "look to cut costs",
                "look to someone for leadership"
            ],
            "usage": {
                "structures": [
                    "look to + sb + for + N (trông cậy vào ai để có được sự chỉ dẫn/hỗ trợ)",
                    "look to + sb + to V (trông cậy vào ai để làm gì)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "look to experts for advice",
                    "look to management for support",
                    "look to new markets",
                    "look to improve efficiency"
                ],
                "tip": "Khi đi với cấu trúc 'look to sb FOR sth', cụm này đồng nghĩa với 'rely on / depend on / turn to sb for sth'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "look",
                    "example": "Investors often look at quarterly earnings before making decisions.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "outlook",
                    "example": "Analysts maintain a favorable outlook on the retail sector.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "onlooker",
                    "example": "A crowd of onlookers gathered for the grand opening ceremony.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "During the corporate restructuring, employees _____ the executive director for clear direction.",
                "answer": "looked to",
                "base_word": "look to",
                "pos_hint": "cụm động từ chia quá khứ đơn",
                "vi": "Trong quá trình tái cơ cấu doanh nghiệp, các nhân viên đã trông cậy vào giám đốc điều hành để có định hướng rõ ràng."
            }
        },
        "loyal": {
            "definition_vi": "trung thành, gắn bó",
            "examples_vi": [
                "Bạn đã là một cố vấn trung thành trong suốt nhiều năm qua, tôi không chắc mình sẽ xoay xở thế nào nếu thiếu bạn.",
                "Mặc dù trợ lý của bạn rất trung thành, bạn vẫn phải đặt câu hỏi về hiệu suất làm việc của anh ta."
            ],
            "collocations": [
                "loyal customer",
                "loyal employee",
                "remain loyal to",
                "customer loyalty"
            ],
            "usage": {
                "structures": [
                    "be/remain loyal to + sb/sth (trung thành/gắn bó với ai/tổ chức nào)"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "fiercely loyal",
                    "brand loyalty",
                    "loyalty program",
                    "reward loyal patrons"
                ],
                "tip": "Cả tính từ 'loyal' và danh từ 'loyalty' đều đi với giới từ 'to'; cụm 'customer loyalty program' (chương trình khách hàng thân thiết) cực kỳ phổ biến trong TOEIC."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "disloyal",
                    "example": "Sharing proprietary data with a competitor is a disloyal and unlawful act.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The airline introduced a new frequent-flyer tier to reward customer _____.",
                "answer": "loyalty",
                "base_word": "loyal",
                "pos_hint": "danh từ",
                "vi": "Hãng hàng không đã giới thiệu một hạng thẻ khách hàng thường xuyên mới nhằm tưởng thưởng cho lòng trung thành của khách hàng."
            }
        },
        "merit": {
            "definition_vi": "(n) công trạng, phẩm chất xứng đáng, giá trị; (v) xứng đáng nhận",
            "examples_vi": [
                "Nhân viên được đánh giá dựa trên năng lực thực chất chứ không phải theo thâm niên.",
                "Công việc của bạn đã cải thiện vượt bậc và có giá trị rất lớn."
            ],
            "collocations": [
                "on one's own merit",
                "merit pay",
                "evaluate on merit",
                "certificate of merit"
            ],
            "usage": {
                "structures": [
                    "on the merits of + N / on one's own merit (dựa trên năng lực/giá trị thực chất)",
                    "merit + consideration/attention (xứng đáng được xem xét/chú ý)"
                ],
                "prepositions": ["on", "of"],
                "collocations": [
                    "merit-based promotion",
                    "merit increase",
                    "artistic merit",
                    "judge each case on its merits"
                ],
                "tip": "Trong chủ đề nhân sự TOEIC, 'merit' thường đối lập với 'seniority' (thâm niên) và xuất hiện trong cụm 'merit raise / merit bonus' (thưởng/tăng lương theo năng lực)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "merit",
                    "example": "The engineer's cost-saving proposal certainly merits serious consideration.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "merit",
                    "example": "Promotions at our firm are awarded strictly on the basis of merit.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "meritorious",
                    "example": "She received a medal for twenty years of meritorious service to the agency.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The safety committee's recommendations _____ immediate attention from factory management.",
                "answer": "merit",
                "base_word": "merit",
                "pos_hint": "động từ chia hiện tại đơn",
                "vi": "Các khuyến nghị của ủy ban an toàn xứng đáng nhận được sự quan tâm ngay lập tức từ ban quản lý nhà máy."
            }
        },
        "obviously": {
            "definition_vi": "rõ ràng là, hiển nhiên là",
            "examples_vi": [
                "Việc đi trễ của cô ấy rõ ràng đã khiến các đồng nghiệp bất bình.",
                "Đây hiển nhiên không phải là lần đầu tiên khách hàng gặp trục trặc với mẫu máy chà nhám cụ thể này."
            ],
            "collocations": [
                "obviously pleased",
                "obviously beneficial",
                "quite obviously",
                "obviously mistaken"
            ],
            "usage": {
                "structures": [
                    "Obviously, + S + V (Rõ ràng là...)",
                    "be + obviously + adj/V3/V-ing (rõ ràng là...)"
                ],
                "prepositions": [],
                "collocations": [
                    "for obvious reasons",
                    "obvious choice",
                    "state the obvious",
                    "become obvious"
                ],
                "tip": "Thường đứng đầu câu (ngăn cách bằng dấu phẩy) hoặc đứng sau động từ 'to be' để nhấn mạnh tính hiển nhiên của sự việc."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "obviousness",
                    "example": "Despite the obviousness of the error, it went unnoticed until the final audit.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "obvious",
                    "example": "It was obvious from the sales report that the new campaign was working.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "obviously",
                    "example": "The client was obviously delighted with the redesigned website.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "With her extensive international experience, Ms. Chen was the _____ choice to lead the overseas branch.",
                "answer": "obvious",
                "base_word": "obviously",
                "pos_hint": "tính từ",
                "vi": "Với kinh nghiệm quốc tế sâu rộng của mình, bà Chen là sự lựa chọn hiển nhiên để dẫn dắt chi nhánh nước ngoài."
            }
        },
        "productive": {
            "definition_vi": "năng suất, hiệu quả, sinh lợi nhiều",
            "examples_vi": [
                "Nhà nghiên cứu đã không làm việc năng suất như vậy khi ông mới bắt đầu làm việc tại đây.",
                "Các nhà quản lý đã có một cuộc họp rất hiệu quả và giải quyết được nhiều vấn đề."
            ],
            "collocations": [
                "productive meeting",
                "highly productive",
                "productive workforce",
                "increase productivity"
            ],
            "usage": {
                "structures": [
                    "be productive (có năng suất / đạt hiệu quả cao)",
                    "a productive meeting/session/discussion (một cuộc họp/buổi thảo luận hiệu quả)"
                ],
                "prepositions": ["of", "for"],
                "collocations": [
                    "productive use of time",
                    "productive relationship",
                    "workplace productivity",
                    "counterproductive"
                ],
                "tip": "Phân biệt hai danh từ trong họ từ: 'production' (sự sản xuất/sản lượng) và 'productivity' (năng suất làm việc)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "productivity",
                    "example": "Upgrading the factory machinery boosted overall worker productivity by fifteen percent.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "productively",
                    "example": "The two departments worked productively together to meet the tight deadline.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Allowing employees to work remotely two days a week has noticeably improved overall _____.",
                "answer": "productivity",
                "base_word": "productive",
                "pos_hint": "danh từ chỉ năng suất",
                "vi": "Việc cho phép nhân viên làm việc từ xa hai ngày một tuần đã cải thiện đáng kể năng suất tổng thể."
            }
        },
        "promote": {
            "definition_vi": "thăng chức; quảng bá, thúc đẩy",
            "examples_vi": [
                "Mặc dù nhân viên bán hàng đã có một năm làm việc tốt, vẫn không thể thăng chức cho anh ấy.",
                "Phó giám đốc đã lan truyền ý kiến cho rằng giám đốc là người thiếu năng lực."
            ],
            "collocations": [
                "promote to manager",
                "promote a new product",
                "promote growth",
                "earn a promotion"
            ],
            "usage": {
                "structures": [
                    "be promoted to + N (được thăng chức lên vị trí gì)",
                    "promote + a product/service/event (quảng bá sản phẩm/dịch vụ/sự kiện)"
                ],
                "prepositions": ["to", "from"],
                "collocations": [
                    "promote from within",
                    "promotional campaign",
                    "sales promotion",
                    "promote teamwork"
                ],
                "tip": "Mang 2 nghĩa cốt lõi trong TOEIC: (1) thăng chức (thường chia bị động 'be promoted to + chức vụ') và (2) quảng bá/thúc đẩy doanh số (promotional offers)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "promotional",
                    "example": "Visitors to our trade show booth will receive free promotional merchandise.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The marketing team distributed _____ flyers to announce the grand opening of the downtown store.",
                "answer": "promotional",
                "base_word": "promote",
                "pos_hint": "tính từ",
                "vi": "Đội ngũ tiếp thị đã phát tờ rơi quảng cáo để thông báo lễ khai trương cửa hàng ở trung tâm thành phố."
            }
        },
        "recognition": {
            "definition_vi": "sự công nhận, sự ghi nhận, sự tuyên dương",
            "examples_vi": [
                "Trợ lý cá nhân của chủ tịch cuối cùng cũng nhận được sự ghi nhận mà cô ấy xứng đáng có được trong nhiều năm qua.",
                "Việc ghi nhận thành tích làm việc xuất sắc nên là việc làm thường xuyên của mọi nhà quản lý."
            ],
            "collocations": [
                "in recognition of",
                "brand recognition",
                "receive recognition",
                "employee recognition"
            ],
            "usage": {
                "structures": [
                    "in recognition of + N (để ghi nhận/tuyên dương cái gì)",
                    "gain/receive recognition for + N (nhận được sự công nhận về điều gì)"
                ],
                "prepositions": ["in", "of", "for"],
                "collocations": [
                    "international recognition",
                    "deserve recognition",
                    "voice recognition",
                    "recognition award"
                ],
                "tip": "Cụm giới từ 'in recognition of + [thành tích/sự cống hiến]' xuất hiện rất nhiều trong các bài phát biểu trao giải và thông báo nội bộ TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "recognize",
                    "example": "The annual banquet is held to recognize employees who have served for ten years.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "recognition",
                    "example": "She was given a bonus in recognition of her exceptional leadership.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "recognizable",
                    "example": "The company's new logo is instantly recognizable to consumers worldwide.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "recognizably",
                    "example": "The redesigned model is recognizably more fuel-efficient than its predecessor.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The CEO presented Mr. Gomez with a gold watch to _____ his three decades of dedicated service.",
                "answer": "recognize",
                "base_word": "recognition",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Giám đốc điều hành đã trao tặng ông Gomez một chiếc đồng hồ vàng để ghi nhận ba thập kỷ cống hiến tận tụy của ông."
            }
        },
        "value": {
            "definition_vi": "(v) định giá; coi trọng, trân trọng; (n) giá trị",
            "examples_vi": [
                "Các nhân viên luôn coi trọng ý kiến của đồng nghiệp mình.",
                "Chuyên gia đã định giá văn bản cổ đó ở mức 7.000 đô la."
            ],
            "collocations": [
                "value someone's opinion",
                "value the property at",
                "market value",
                "valued customer"
            ],
            "usage": {
                "structures": [
                    "value + sth + at + [số tiền] (định giá cái gì ở mức bao nhiêu)",
                    "value + sb/sth (trân trọng/đánh giá cao ai/cái gì)"
                ],
                "prepositions": ["at", "for"],
                "collocations": [
                    "highly valued employee",
                    "core values",
                    "good value for money",
                    "decline in value"
                ],
                "tip": "Chú ý phân biệt: 'valuable' (có giá trị lớn/quý giá), 'invaluable' (vô giá = cực kỳ quý giá), 'valueless' (vô giá trị), và 'valued' (được trân trọng: a valued client)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "value",
                    "example": "We deeply value the feedback provided by our long-term clients.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "valuation",
                    "example": "An independent appraiser completed a valuation of the commercial property.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "valuable",
                    "example": "Internships provide students with valuable hands-on industry experience.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "valued",
                    "example": "As a valued member of our rewards program, you qualify for free shipping.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Thank you for being a _____ customer of Apex Telecommunications over the past five years.",
                "answer": "valued",
                "base_word": "value",
                "pos_hint": "tính từ (V-ed) bổ nghĩa cho customer",
                "vi": "Cảm ơn quý khách đã là một khách hàng đáng trân trọng của Viễn thông Apex trong suốt năm năm qua."
            }
        }
    },
    16: {
        "bargain": {
            "definition_vi": "(v) mặc cả, thương lượng giá; (n) món hời, mặt hàng giá rẻ",
            "examples_vi": [
                "Cô ấy đã mặc cả hơn một tiếng đồng hồ và cuối cùng giảm được một nửa giá.",
                "Lois đã so sánh những chiếc áo len một cách cẩn thận để xác định xem chiếc nào là món hời tốt hơn."
            ],
            "collocations": [
                "a real bargain",
                "bargain price",
                "bargain for a lower price",
                "collective bargaining"
            ],
            "usage": {
                "structures": [
                    "bargain with + sb + over/for + sth (mặc cả/thương lượng với ai về cái gì)",
                    "at a bargain price (ở mức giá hời)"
                ],
                "prepositions": ["with", "for", "over", "at"],
                "collocations": [
                    "bargain hunter",
                    "strike a bargain",
                    "into the bargain",
                    "bargain basement"
                ],
                "tip": "Danh từ 'bargain' thường đi với tính từ 'good/great/real' (a great bargain = một món hời lớn) hoặc đứng trước 'price' (bargain prices)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "bargain",
                    "example": "Tourists often bargain with street vendors at the local market.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "bargain",
                    "example": "At fifty percent off, this winter coat is an absolute bargain.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "bargaining",
                    "example": "Another round of collective bargaining will begin next Monday.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Shoppers arrived early in the morning to hunt for _____ during the annual clearance sale.",
                "answer": "bargains",
                "base_word": "bargain",
                "pos_hint": "danh từ số nhiều",
                "vi": "Người mua sắm đã đến từ sáng sớm để săn lùng những món hời trong đợt giảm giá xả kho thường niên."
            }
        },
        "bear": {
            "definition_vi": "chịu đựng; gánh vác (chi phí/trách nhiệm)",
            "examples_vi": [
                "Moya không thích đám đông nên cô không thể chịu đựng được việc đi mua sắm vào dịp cao điểm lễ hội.",
                "Nếu bạn có thể kiên nhẫn chờ tôi một chút, tôi muốn ghé thêm một cửa hàng nữa."
            ],
            "collocations": [
                "bear with someone",
                "bear in mind",
                "bear the cost",
                "cannot bear to"
            ],
            "usage": {
                "structures": [
                    "bear with + sb (kiên nhẫn chờ/thông cảm cho ai)",
                    "bear in mind (that) (ghi nhớ rằng)",
                    "bear the cost/responsibility (chịu chi phí/trách nhiệm)"
                ],
                "prepositions": ["with", "in"],
                "collocations": [
                    "bear the expense",
                    "bear a resemblance to",
                    "bear witness to",
                    "more than one can bear"
                ],
                "tip": "Trong TOEIC Listening và Reading, cụm lịch sự 'Please bear with us while we...' (Xin hãy kiên nhẫn chờ chúng tôi trong khi...) và 'bear the cost' (chịu chi phí) xuất hiện rất nhiều."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "bear",
                    "example": "The manufacturer agreed to bear the full cost of replacing the faulty parts.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "bearer",
                    "example": "This voucher entitles the bearer to a ten-dollar discount on any purchase.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "bearable",
                    "example": "Installing air conditioning made working in the warehouse much more bearable.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "unbearable",
                    "example": "The noise from the adjacent construction site became unbearable by noon.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Under the terms of the warranty, the buyer must _____ the shipping charges for returned merchandise.",
                "answer": "bear",
                "base_word": "bear",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Theo các điều khoản bảo hành, người mua phải chịu phí vận chuyển đối với hàng hóa trả lại."
            }
        },
        "behavior": {
            "definition_vi": "hành vi, cách cư xử, thái độ",
            "examples_vi": [
                "Annu đang tiến hành một cuộc khảo sát xem liệu hành vi tiêu dùng có khác biệt giữa nam giới và nữ giới hay không.",
                "Hành vi đáng ngờ trong cửa hàng bách hóa sẽ thu hút sự chú ý của các nhân viên bảo vệ."
            ],
            "collocations": [
                "consumer behavior",
                "buying behavior",
                "professional behavior",
                "unacceptable behavior"
            ],
            "usage": {
                "structures": [
                    "behavior toward + sb (cách cư xử đối với ai)",
                    "consumer/customer behavior (hành vi của người tiêu dùng)"
                ],
                "prepositions": ["toward", "of"],
                "collocations": [
                    "purchasing behavior",
                    "ethical behavior",
                    "code of behavior",
                    "study market behavior"
                ],
                "tip": "Danh từ không đếm được, rất hay kết hợp thành cụm danh từ ghép 'consumer behavior / purchasing behavior' trong chủ đề Marketing & Purchasing."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "behave",
                    "example": "All representatives are expected to behave professionally at trade fairs.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "behavior",
                    "example": "Recent surveys show a shift in online shopping behavior.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "behavioral",
                    "example": "The marketing firm analyzes behavioral data to predict seasonal trends.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "behaviorally",
                    "example": "Loyalty members differ behaviorally from occasional bargain shoppers.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The research team used _____ analytics to understand how shoppers navigate the online store.",
                "answer": "behavioral",
                "base_word": "behavior",
                "pos_hint": "tính từ",
                "vi": "Nhóm nghiên cứu đã sử dụng phân tích hành vi để tìm hiểu cách người mua sắm điều hướng trên cửa hàng trực tuyến."
            }
        },
        "checkout": {
            "definition_vi": "quầy thanh toán; thủ tục/giờ trả phòng (khách sạn)",
            "examples_vi": [
                "Hàng người chờ ở quầy thanh toán này quá dài, vì vậy chúng ta hãy tìm một quầy khác.",
                "Bạn cứ xếp hàng ở quầy thanh toán ngay bây giờ đi và tôi sẽ mang những món đồ cuối cùng ra chỗ bạn."
            ],
            "collocations": [
                "checkout counter",
                "checkout line",
                "express checkout",
                "late checkout"
            ],
            "usage": {
                "structures": [
                    "at the checkout (counter) (tại quầy thanh toán)",
                    "checkout time (giờ trả phòng khách sạn)"
                ],
                "prepositions": ["at"],
                "collocations": [
                    "checkout aisle",
                    "self-service checkout",
                    "online checkout process",
                    "checkout clerk"
                ],
                "tip": "Viết liền 'checkout' là danh từ (quầy thanh toán/thủ tục trả phòng), còn viết rời 'check out' là cụm động từ (thanh toán / trả phòng / kiểm tra)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "check out",
                    "example": "Hotel guests must check out before eleven o'clock in the morning.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "checkout",
                    "example": "Please present your discount coupon to the cashier at the checkout.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Supermarket patrons with ten items or fewer may use the express _____ lane.",
                "answer": "checkout",
                "base_word": "checkout",
                "pos_hint": "danh từ bổ nghĩa",
                "vi": "Khách hàng siêu thị mua từ mười món đồ trở xuống có thể sử dụng làn thanh toán nhanh."
            }
        },
        "comfort": {
            "definition_vi": "(n) sự thoải mái, sự tiện nghi; (v) an ủi, làm dịu lại",
            "examples_vi": [
                "Hãy tự mang lại sự ấm áp dễ chịu cho bản thân bằng một chiếc chăn lông vũ vào mùa đông này.",
                "Tôi thích ăn mặc sao cho thoải mái nếu phải dành cả ngày để đi mua sắm."
            ],
            "collocations": [
                "for comfort",
                "in comfort",
                "creature comforts",
                "comfort zone"
            ],
            "usage": {
                "structures": [
                    "dress for comfort (mặc đồ ưu tiên sự thoải mái)",
                    "travel in comfort (di chuyển một cách tiện nghi, thoải mái)"
                ],
                "prepositions": ["for", "in", "with"],
                "collocations": [
                    "designed for maximum comfort",
                    "comfortable seating",
                    "comfortably furnished",
                    "take comfort in"
                ],
                "tip": "Họ từ này rất hay xuất hiện trong quảng cáo ghế văn phòng, khách sạn, giày dép và phương tiện vận chuyển (designed for your comfort / comfortably seats six)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "uncomfortable",
                    "example": "Employees complained that the old desk chairs were uncomfortable.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The newly renovated airport lounge features _____ leather armchairs and complimentary Wi-Fi.",
                "answer": "comfortable",
                "base_word": "comfort",
                "pos_hint": "tính từ",
                "vi": "Phòng chờ sân bay mới được tân trang có những chiếc ghế bành bọc da êm ái và Wi-Fi miễn phí."
            }
        },
        "expand": {
            "definition_vi": "mở rộng, phát triển thêm",
            "examples_vi": [
                "Người quản lý mới đã mở rộng đáng kể lượng hàng hóa lưu kho của cửa hàng.",
                "Cửa hàng giày đã hết chỗ và đang cân nhắc việc mở rộng sang tòa nhà trống liền kề."
            ],
            "collocations": [
                "expand into new markets",
                "expand the product line",
                "expand operations",
                "rapid expansion"
            ],
            "usage": {
                "structures": [
                    "expand + into + N (mở rộng sang thị trường/khu vực mới)",
                    "expand + O (mở rộng quy mô/danh mục sản phẩm)"
                ],
                "prepositions": ["into", "by", "beyond"],
                "collocations": [
                    "expand business overseas",
                    "expansion plan",
                    "expand capacity",
                    "expanding client base"
                ],
                "tip": "Đi với giới từ 'into' khi nói về việc mở rộng hoạt động kinh doanh sang một thị trường, lĩnh vực hoặc mặt bằng mới (expand into Asia)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "expansive",
                    "example": "The hotel suite offers an expansive view of the harbor.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "expansively",
                    "example": "The CEO spoke expansively about the company's five-year growth strategy.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Following strong domestic sales, the apparel retailer announced plans for international _____.",
                "answer": "expansion",
                "base_word": "expand",
                "pos_hint": "danh từ",
                "vi": "Tiếp nối doanh số nội địa mạnh mẽ, nhà bán lẻ trang phục đã công bố kế hoạch mở rộng ra quốc tế."
            }
        },
        "explore": {
            "definition_vi": "khám phá, tìm hiểu, thăm dò, khảo sát",
            "examples_vi": [
                "Nhà sưu tập thích dạo quanh khám phá các cửa hàng đồ cổ để tìm kiếm những món hời.",
                "Trong khi mẹ mua quần áo, Michael đã đi sang khám phá khu vực đồ chơi."
            ],
            "collocations": [
                "explore new possibilities",
                "explore options",
                "explore a market",
                "explore ways to"
            ],
            "usage": {
                "structures": [
                    "explore + possibilities/options/opportunities (tìm hiểu các khả năng/lựa chọn/cơ hội)",
                    "explore + ways to V (tìm kiếm các cách thức để làm gì)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "explore potential partnerships",
                    "exploratory talks",
                    "explore every avenue",
                    "market exploration"
                ],
                "tip": "Trong tiếng Anh thương mại, 'explore' thường mang nghĩa bóng là 'nghiên cứu, thăm dò' các phương án hoặc cơ hội hợp tác (explore business opportunities)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "explorer",
                    "example": "Early market explorers often gain a strong competitive advantage.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The two pharmaceutical companies held _____ discussions regarding a possible joint venture.",
                "answer": "exploratory",
                "base_word": "explore",
                "pos_hint": "tính từ",
                "vi": "Hai công ty dược phẩm đã tổ chức các cuộc thảo luận thăm dò liên quan đến một liên doanh tiềm năng."
            }
        },
        "item": {
            "definition_vi": "món hàng, mặt hàng; mục, khoản",
            "examples_vi": [
                "Cửa hàng tạp hóa có một làn thanh toán đặc biệt dành cho những người mua ít hơn mười món hàng.",
                "Bạn có nghĩ tôi có thể cho hết tất cả những món đồ này vào một chiếc túi không?"
            ],
            "collocations": [
                "sale item",
                "item on the agenda",
                "defective item",
                "itemized receipt"
            ],
            "usage": {
                "structures": [
                    "an item on the agenda/list (một mục trong chương trình nghị sự / danh sách)",
                    "household/luxury/promotional items (các mặt hàng gia dụng/xa xỉ/khuyến mãi)"
                ],
                "prepositions": ["on", "in"],
                "collocations": [
                    "complimentary item",
                    "next item on the agenda",
                    "out-of-stock item",
                    "individual items"
                ],
                "tip": "Là danh từ đếm được (a single item / ten items), trái ngược với 'merchandise' là danh từ không đếm được."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "itemize",
                    "example": "Contractors must itemize all labor and material costs on the invoice.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "itemization",
                    "example": "The client requested a full itemization of the consulting expenses.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "itemized",
                    "example": "Employees must attach an itemized receipt to every reimbursement claim.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "For tax purposes, please request an _____ bill from the hotel front desk upon checkout.",
                "answer": "itemized",
                "base_word": "item",
                "pos_hint": "tính từ (V-ed)",
                "vi": "Vì mục đích thuế, vui lòng yêu cầu hóa đơn liệt kê chi tiết từng khoản từ quầy lễ tân khách sạn khi trả phòng."
            }
        },
        "mandatory": {
            "definition_vi": "bắt buộc, theo quy định",
            "examples_vi": [
                "Cửa hàng trang sức có chính sách bắt buộc là mỗi lần chỉ cho khách hàng xem một món đồ.",
                "Có quy định giới hạn bắt buộc là chín món hàng khi sử dụng làn thanh toán này."
            ],
            "collocations": [
                "mandatory training",
                "mandatory attendance",
                "mandatory requirement",
                "mandatory inspection"
            ],
            "usage": {
                "structures": [
                    "be mandatory for + sb (to V) (bắt buộc đối với ai phải làm gì)",
                    "mandatory + N (meeting/training/retirement) (buổi họp/đào tạo/nghỉ hưu bắt buộc)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "mandatory safety gear",
                    "mandatory overtime",
                    "make it mandatory",
                    "mandatory policy"
                ],
                "tip": "Đồng nghĩa với 'compulsory, obligatory, required' và trái nghĩa với 'optional, voluntary' trong các câu hỏi từ vựng TOEIC."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "mandatorily",
                    "example": "All food-handling personnel are mandatorily tested for hygiene compliance.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "New federal regulations _____ that all commercial vehicles undergo emission testing twice a year.",
                "answer": "mandate",
                "base_word": "mandatory",
                "pos_hint": "động từ chia hiện tại đơn",
                "vi": "Các quy định liên bang mới bắt buộc tất cả các phương tiện thương mại phải trải qua kiểm tra khí thải hai lần một năm."
            }
        },
        "merchandise": {
            "definition_vi": "(n) hàng hóa (bày bán); (v) kinh doanh, tiếp thị hàng hóa",
            "examples_vi": [
                "Tôi rất ấn tượng với sự đa dạng hàng hóa tại cửa hàng này.",
                "Helen muốn đảm bảo rằng cửa hàng có nhiều chủng loại hàng hóa phong phú trước khi quyết định mua phiếu quà tặng."
            ],
            "collocations": [
                "display merchandise",
                "defective merchandise",
                "return merchandise",
                "wide variety of merchandise"
            ],
            "usage": {
                "structures": [
                    "a wide selection/variety of merchandise (nhiều chủng loại hàng hóa đa dạng)"
                ],
                "prepositions": ["of"],
                "collocations": [
                    "damaged merchandise",
                    "promotional merchandise",
                    "general merchandise",
                    "merchandise Mart"
                ],
                "tip": "Cực kỳ quan trọng: 'merchandise' là DANH TỪ KHÔNG ĐẾM ĐƯỢC (không bao giờ có -s hay a/an), luôn đồng nghĩa với 'goods, wares, items'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "merchandising",
                    "example": "Effective visual merchandising can significantly boost impulse purchases.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Local _____ in the historic district agreed to extend their opening hours during the summer festival.",
                "answer": "merchants",
                "base_word": "merchandise",
                "pos_hint": "danh từ chỉ người (thương nhân/chủ cửa hàng) số nhiều",
                "vi": "Các chủ cửa hàng địa phương trong khu phố cổ đã đồng ý kéo dài giờ mở cửa trong suốt lễ hội mùa hè."
            }
        },
        "strictly": {
            "definition_vi": "một cách nghiêm ngặt, chặt chẽ, tuyệt đối",
            "examples_vi": [
                "Cửa hàng của chúng tôi thực thi chính sách đổi trả hàng một cách nghiêm ngặt.",
                "Tỷ lệ nghỉ việc cao của họ không có gì đáng ngạc nhiên khi xét đến việc người quản lý đối xử khắt khe với họ như thế nào."
            ],
            "collocations": [
                "strictly prohibited",
                "strictly enforced",
                "strictly confidential",
                "strictly adhere to"
            ],
            "usage": {
                "structures": [
                    "be strictly prohibited/forbidden/enforced (bị nghiêm cấm tuyệt đối / được thực thi nghiêm ngặt)",
                    "strictly confidential (tuyệt mật)"
                ],
                "prepositions": [],
                "collocations": [
                    "strictly speaking",
                    "strictly limited",
                    "strictly regulated",
                    "strictly comply with"
                ],
                "tip": "Ba cụm từ tủ trong đề thi TOEIC: 'strictly prohibited' (nghiêm cấm), 'strictly confidential' (tuyệt mật), và 'strictly enforced' (được thực thi nghiêm ngặt)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "restrict",
                    "example": "Access to the server room is restricted to authorized IT personnel.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All laboratories must adhere to _____ safety guidelines when handling chemical samples.",
                "answer": "strict",
                "base_word": "strictly",
                "pos_hint": "tính từ",
                "vi": "Tất cả các phòng thí nghiệm phải tuân thủ các hướng dẫn an toàn nghiêm ngặt khi xử lý mẫu hóa chất."
            }
        },
        "trend": {
            "definition_vi": "(n) xu hướng, trào lưu; (v) có xu hướng",
            "examples_vi": [
                "Cửa hàng quần áo cố gắng nắm bắt dẫn đầu tất cả các xu hướng mới.",
                "Mioshi đã theo dõi sát sao các xu hướng thị trường trước khi cô mua nhượng quyền một thương hiệu quần áo."
            ],
            "collocations": [
                "market trend",
                "current trend",
                "set a trend",
                "upward trend"
            ],
            "usage": {
                "structures": [
                    "trend toward + N (xu hướng nghiêng về cái gì)",
                    "trend in + N (xu hướng trong lĩnh vực gì)"
                ],
                "prepositions": ["toward", "in"],
                "collocations": [
                    "downward trend",
                    "industry trends",
                    "follow a trend",
                    "economic trends"
                ],
                "tip": "Thường đi với các tính từ chỉ chiều hướng biến động trên biểu đồ báo cáo như 'upward/downward/recent/current/emerging trend'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "trend",
                    "example": "Raw material prices have been trending upward over the past six months.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "trend",
                    "example": "The report analyzes recent trends in e-commerce logistics.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "trendy",
                    "example": "The boutique attracts young shoppers with its trendy accessories.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The newly opened café quickly became popular among young professionals for its _____ decor.",
                "answer": "trendy",
                "base_word": "trend",
                "pos_hint": "tính từ",
                "vi": "Quán cà phê mới mở nhanh chóng trở nên nổi tiếng trong giới chuyên gia trẻ nhờ lối trang trí thời thượng."
            }
        }
    },
    17: {
        "diversify": {
            "definition_vi": "đa dạng hóa",
            "examples_vi": [
                "Bộ phận văn phòng phẩm có kế hoạch đa dạng hóa các mặt hàng sản phẩm giấy của mình.",
                "Chuyên gia tư vấn mà chúng tôi đã thuê khuyến nghị rằng chúng tôi không nên đa dạng hóa vào thời điểm này."
            ],
            "collocations": [
                "diversify the product line",
                "diversify into new markets",
                "diversified portfolio",
                "workplace diversity"
            ],
            "usage": {
                "structures": [
                    "diversify + O (product line / portfolio / offerings) (đa dạng hóa dòng sản phẩm / danh mục đầu tư)",
                    "diversify into + N (đa dạng hóa sang lĩnh vực gì)"
                ],
                "prepositions": ["into"],
                "collocations": [
                    "diverse range of products",
                    "cultural diversity",
                    "diversify revenue streams",
                    "business diversification"
                ],
                "tip": "Tính từ 'diverse' rất hay đi trong cụm 'a diverse range/array/group of + danh từ số nhiều' (một loạt đa dạng các...)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "diversification",
                    "example": "Market diversification helped the manufacturer survive the regional downturn.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "diversely",
                    "example": "The conglomerate's assets are diversely distributed across four continents.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The supplier offers a _____ selection of eco-friendly packaging materials.",
                "answer": "diverse",
                "base_word": "diversify",
                "pos_hint": "tính từ",
                "vi": "Nhà cung cấp mang đến sự lựa chọn đa dạng các vật liệu đóng gói thân thiện với môi trường."
            }
        },
        "enterprise": {
            "definition_vi": "doanh nghiệp, xí nghiệp; dự án lớn",
            "examples_vi": [
                "Doanh nghiệp mới đã nhanh chóng thiết lập một tài khoản khách hàng với cửa hàng văn phòng phẩm.",
                "Doanh nghiệp này đã trở nên không thể quản lý nổi và đang bắt đầu thua lỗ."
            ],
            "collocations": [
                "commercial enterprise",
                "private enterprise",
                "small and medium-sized enterprises",
                "joint enterprise"
            ],
            "usage": {
                "structures": [
                    "free/private/commercial enterprise (doanh nghiệp tự do/tư nhân/thương mại)"
                ],
                "prepositions": ["in", "of"],
                "collocations": [
                    "state-owned enterprise",
                    "enterprise software",
                    "enterprising spirit",
                    "global enterprise"
                ],
                "tip": "Tính từ 'enterprising' trong họ từ này mang nghĩa là 'dám nghĩ dám làm, năng động, có tinh thần khởi nghiệp'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "enterprisingly",
                    "example": "She enterprisingly turned a local delivery service into a national logistics firm.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The chamber of commerce awards grants to _____ young business owners every autumn.",
                "answer": "enterprising",
                "base_word": "enterprise",
                "pos_hint": "tính từ",
                "vi": "Phòng thương mại trao các khoản tài trợ cho những chủ doanh nghiệp trẻ năng động vào mỗi mùa thu."
            }
        },
        "essentially": {
            "definition_vi": "về cơ bản, về bản chất, thực chất là",
            "examples_vi": [
                "Về cơ bản, cô ấy muốn giành được hợp đồng và loại đối thủ cạnh tranh ra khỏi cuộc chơi.",
                "Sau khi phân phát tất cả các hộp mực đã đặt mua, thực chất chúng tôi chẳng còn lại hộp nào."
            ],
            "collocations": [
                "essentially the same",
                "essentially unchanged",
                "essential to success",
                "essential supplies"
            ],
            "usage": {
                "structures": [
                    "be essential to/for + N (thiết yếu đối với cái gì)",
                    "It is essential that + S + (should) + V-inf (Điều thiết yếu là...)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "essential equipment",
                    "essentially identical",
                    "in essence",
                    "of the essence"
                ],
                "tip": "Tính từ 'essential' kích hoạt cấu trúc giả định cách: 'It is essential that every employee wear/submit...' (động từ nguyên mẫu không chia)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "essentials",
                    "example": "The small store stocks office essentials such as paper, pens, and toner.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Reliable high-speed internet access is _____ for companies operating cloud-based inventory systems.",
                "answer": "essential",
                "base_word": "essentially",
                "pos_hint": "tính từ",
                "vi": "Kết nối internet tốc độ cao ổn định là điều thiết yếu đối với các công ty vận hành hệ thống kiểm kê đám mây."
            }
        },
        "everyday": {
            "definition_vi": "hằng ngày, thông thường, thường nhật",
            "examples_vi": [
                "Mặc dù đắt hơn, những bìa kẹp hồ sơ này sẽ chịu được sự hao mòn trong sử dụng hằng ngày.",
                "Công việc lặp đi lặp lại hằng ngày là phải kiểm tra hàng tồn kho này thật nhàm chán."
            ],
            "collocations": [
                "everyday use",
                "everyday routine",
                "everyday wear and tear",
                "everyday operations"
            ],
            "usage": {
                "structures": [
                    "everyday + N (tính từ luôn đứng trước danh từ: everyday life/use/tasks)"
                ],
                "prepositions": ["in"],
                "collocations": [
                    "everyday business activities",
                    "everyday low prices",
                    "everyday occurrences",
                    "everyday items"
                ],
                "tip": "Phân biệt: viết liền 'everyday' là TÍNH TỪ đứng trước danh từ (everyday tasks), còn viết rời 'every day' là cụm trạng từ chỉ thời gian thường đứng cuối câu."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "day",
                    "example": "Orders placed before noon are shipped the same day.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "everyday",
                    "example": "Durable laminating machines are built to handle heavy everyday use.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "daily",
                    "example": "The warehouse supervisor conducts a daily inspection of the forklifts.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "daily",
                    "example": "Supply levels are monitored daily to prevent unexpected shortages.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "This heavy-duty photocopier is designed to withstand the demands of _____ office use.",
                "answer": "everyday",
                "base_word": "everyday",
                "pos_hint": "tính từ ghép",
                "vi": "Chiếc máy photocopy công suất lớn này được thiết kế để chịu được nhu cầu sử dụng văn phòng hằng ngày."
            }
        },
        "function": {
            "definition_vi": "(v) hoạt động, vận hành, đóng vai trò; (n) chức năng, sự kiện trang trọng",
            "examples_vi": [
                "Cô ấy đã đảm nhiệm vai trò giám đốc trong thời gian ông Gibbs đi vắng.",
                "Chức năng của thiết bị này là gì?"
            ],
            "collocations": [
                "function properly",
                "function as",
                "official function",
                "fully functional"
            ],
            "usage": {
                "structures": [
                    "function as + N (đóng vai trò/hoạt động như là cái gì)",
                    "corporate/social function (buổi tiệc/sự kiện trang trọng của công ty)"
                ],
                "prepositions": ["as"],
                "collocations": [
                    "perform a function",
                    "vital function",
                    "banquet and function rooms",
                    "function smoothly"
                ],
                "tip": "Lưu ý nghĩa thứ hai rất hay ra trong TOEIC: ngoài nghĩa 'chức năng', danh từ đếm được 'a function' còn có nghĩa là 'một buổi tiệc/sự kiện trang trọng' (corporate functions)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "functionality",
                    "example": "The latest software update adds new search functionality.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "functionally",
                    "example": "Though different in appearance, the two scanner models are functionally identical.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The backup generator failed to _____ properly during yesterday's power outage.",
                "answer": "function",
                "base_word": "function",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Máy phát điện dự phòng đã không hoạt động bình thường trong sự cố mất điện ngày hôm qua."
            }
        },
        "maintain": {
            "definition_vi": "duy trì, giữ gìn; bảo trì, bảo dưỡng; khẳng định",
            "examples_vi": [
                "Tôi vẫn đang duy trì một danh sách các vật tư văn phòng có nhu cầu lớn nhất.",
                "Việc cố gắng duy trì hai kho chứa hàng khác nhau là quá nhiều việc."
            ],
            "collocations": [
                "maintain records",
                "maintain equipment",
                "maintain high standards",
                "routine maintenance"
            ],
            "usage": {
                "structures": [
                    "maintain + N (duy trì mối quan hệ/tiêu chuẩn/hồ sơ; bảo dưỡng máy móc)",
                    "maintain that + S + V (khẳng định rằng...)"
                ],
                "prepositions": ["at", "in"],
                "collocations": [
                    "maintain a competitive edge",
                    "maintain close contact",
                    "properly maintained",
                    "maintenance department"
                ],
                "tip": "Danh từ phổ biến nhất của 'maintain' trong bài thi TOEIC là 'maintenance' (chú ý chính tả: main-te-nance, không phải maintainance), nghĩa là sự bảo trì/duy trì."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "maintenance",
                    "example": "Regular maintenance of the printing presses prevents costly breakdowns.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The online ordering portal will be temporarily offline tonight for scheduled system _____.",
                "answer": "maintenance",
                "base_word": "maintain",
                "pos_hint": "danh từ chỉ sự bảo trì",
                "vi": "Cổng đặt hàng trực tuyến sẽ tạm thời ngừng hoạt động vào tối nay để bảo trì hệ thống theo lịch trình."
            }
        },
        "obtain": {
            "definition_vi": "đạt được, lấy được, thu được, xin được",
            "examples_vi": [
                "Tôi đã cố gắng lấy danh sách vật tư từ người quản trị suốt ba tuần nay rồi.",
                "Nhân viên đã lấy được bản báo cáo từ người giám sát của mình."
            ],
            "collocations": [
                "obtain permission",
                "obtain a permit",
                "obtain information",
                "obtain approval"
            ],
            "usage": {
                "structures": [
                    "obtain + sth + from + sb/sth (lấy/xin được cái gì từ ai/đâu)"
                ],
                "prepositions": ["from", "through"],
                "collocations": [
                    "obtain a refund",
                    "obtain a copy",
                    "obtain financing",
                    "easily obtainable"
                ],
                "tip": "Từ trang trọng thay cho 'get' trong văn bản thương mại TOEIC; thường đi với 'permission, approval, permit, license, supplies, information'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "obtain",
                    "example": "Visitors must obtain a security badge at the reception desk.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "obtainable",
                    "example": "Application forms are obtainable from any regional branch office.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "unobtainable",
                    "example": "Replacement parts for the discontinued model are now almost unobtainable.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Contractors must _____ a building permit from the municipal office before commencing renovations.",
                "answer": "obtain",
                "base_word": "obtain",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Các nhà thầu phải xin giấy phép xây dựng từ văn phòng thành phố trước khi bắt đầu việc cải tạo."
            }
        },
        "prerequisite": {
            "definition_vi": "điều kiện tiên quyết, điều kiện cần có trước",
            "examples_vi": [
                "Một trong những điều kiện tiên quyết cho công việc này là năng lực về nghiệp vụ sổ sách kế toán.",
                "Đây là những vật dụng bắt buộc cần có mà bạn phải mua trước khi đến lớp."
            ],
            "collocations": [
                "prerequisite for the job",
                "prerequisite to admission",
                "meet the prerequisites",
                "essential prerequisite"
            ],
            "usage": {
                "structures": [
                    "a prerequisite for/to + N (một điều kiện tiên quyết cho cái gì)"
                ],
                "prepositions": ["for", "to", "of"],
                "collocations": [
                    "prerequisite course",
                    "necessary prerequisite",
                    "fulfill the prerequisites",
                    "basic prerequisite"
                ],
                "tip": "Tiền tố 'pre-' (trước) + 'requisite' (điều cần thiết) = điều kiện bắt buộc phải có trước; luôn đi với giới từ 'for' hoặc 'to'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "require",
                    "example": "All purchase orders over $1,000 require a director's signature.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "prerequisite",
                    "example": "A valid driver's license is a prerequisite for the delivery position.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "requisite",
                    "example": "She lacked the requisite experience to manage the supply chain.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Fluency in Mandarin is a _____ for applicants seeking the regional procurement manager role.",
                "answer": "prerequisite",
                "base_word": "prerequisite",
                "pos_hint": "danh từ",
                "vi": "Sự thông thạo tiếng Quan Thoại là điều kiện tiên quyết đối với các ứng viên ứng tuyển vị trí quản lý thu mua khu vực."
            }
        },
        "quality": {
            "definition_vi": "(n) chất lượng; phẩm chất, đặc tính; (adj) có chất lượng cao",
            "examples_vi": [
                "Những phẩm chất quan trọng nhất mà chúng tôi tìm kiếm ở một nhà cung cấp là độ tin cậy và phản hồi nhanh chóng.",
                "Chất lượng quần áo của họ đã sụt giảm kể từ khi họ bắt đầu sử dụng các loại vải rẻ tiền hơn để may."
            ],
            "collocations": [
                "quality control",
                "quality assurance",
                "superior quality",
                "leadership qualities"
            ],
            "usage": {
                "structures": [
                    "of high/poor/superior quality (có chất lượng cao/kém/vượt trội)",
                    "qualities in + a person/supplier (những phẩm chất ở một người/nhà cung cấp)"
                ],
                "prepositions": ["of", "in"],
                "collocations": [
                    "high-quality materials",
                    "maintain quality standards",
                    "compromise on quality",
                    "personal qualities"
                ],
                "tip": "Khi mang nghĩa 'chất lượng sản phẩm' thì thường không đếm được; khi mang nghĩa 'phẩm chất/đặc tính của một người hay nhà cung cấp' thì là danh từ đếm được (important qualities)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "qualify",
                    "example": "Bulk orders over fifty units qualify for a ten percent discount.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "quality",
                    "example": "Every batch of paper undergoes strict quality inspections.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "qualitative",
                    "example": "The research team conducted a qualitative analysis of customer feedback.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "qualitatively",
                    "example": "The new synthetic fiber is qualitatively superior to previous materials.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Patience and attention to detail are essential _____ for anyone working in inventory management.",
                "answer": "qualities",
                "base_word": "quality",
                "pos_hint": "danh từ số nhiều chỉ phẩm chất",
                "vi": "Sự kiên nhẫn và chú ý đến từng chi tiết là những phẩm chất thiết yếu đối với bất kỳ ai làm việc trong ngành quản lý kho."
            }
        },
        "smooth": {
            "definition_vi": "(adj) suôn sẻ, trôi chảy; lịch thiệp, khéo ăn nói; (v) làm dịu đi, tháo gỡ",
            "examples_vi": [
                "Nhờ quá trình chuyển đổi suôn sẻ sang nhà cung cấp mới của chúng tôi, đã không có sự gián đoạn nào trong các chuyến hàng.",
                "Phong thái khéo léo lịch thiệp của cô đã giúp cô nhận được sự đánh giá cao của người quản lý nhưng lại không được lòng đồng nghiệp."
            ],
            "collocations": [
                "smooth transition",
                "smooth operation",
                "go smoothly",
                "smooth out difficulties"
            ],
            "usage": {
                "structures": [
                    "a smooth transition (sự chuyển giao suôn sẻ)",
                    "run/go/proceed smoothly (diễn ra một cách suôn sẻ)",
                    "smooth out + problems/differences (dàn xếp/tháo gỡ trục trặc)"
                ],
                "prepositions": ["out", "over"],
                "collocations": [
                    "ensure a smooth handover",
                    "smooth implementation",
                    "smooth surface",
                    "work smoothly"
                ],
                "tip": "Cặp từ cực kỳ hay gặp: tính từ 'smooth' đứng trước 'transition / operation' và trạng từ 'smoothly' đi sau các động từ 'go / run / proceed / operate'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "smooth",
                    "example": "The mediator helped smooth relations between the supplier and the buyer.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "smoothness",
                    "example": "This premium printing paper is prized for its brightness and smoothness.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The installation of the new accounting software proceeded _____ thanks to thorough preparation.",
                "answer": "smoothly",
                "base_word": "smooth",
                "pos_hint": "trạng từ",
                "vi": "Việc cài đặt phần mềm kế toán mới đã diễn ra suôn sẻ nhờ sự chuẩn bị kỹ lưỡng."
            }
        },
        "source": {
            "definition_vi": "(n) nguồn, nguồn gốc, nơi cung cấp; (v) tìm nguồn cung ứng",
            "examples_vi": [
                "Tôi không thể tiết lộ cho bạn biết nguồn gốc của thông tin này.",
                "Nguồn gốc của loại gốm quý hiếm mà chúng tôi đang bán trong cửa hàng là một ngôi làng nhỏ ở Ấn Độ."
            ],
            "collocations": [
                "source of information",
                "source of income",
                "reliable source",
                "source materials locally"
            ],
            "usage": {
                "structures": [
                    "source of + N (nguồn cung cấp/nguồn gốc của cái gì)",
                    "source + products/materials + from... (tìm nguồn cung hàng hóa/nguyên liệu từ...)"
                ],
                "prepositions": ["of", "from"],
                "collocations": [
                    "primary source",
                    "energy source",
                    "revenue source",
                    "outsource production"
                ],
                "tip": "Trong chủ đề Purchasing, 'source' vừa là danh từ (nguồn gốc) vừa là động từ mang nghĩa 'tìm nguồn cung ứng' (source raw materials from local farms)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "source",
                    "example": "The bakery sources all of its organic flour from regional mills.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "source",
                    "example": "Tourism is the primary source of revenue for the island's economy.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "sourcing",
                    "example": "Ethical sourcing of raw materials is a core part of our corporate mission.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To reduce shipping costs, the furniture maker began _____ timber from domestic forests.",
                "answer": "sourcing",
                "base_word": "source",
                "pos_hint": "danh động từ (V-ing)",
                "vi": "Để giảm chi phí vận chuyển, nhà sản xuất đồ nội thất đã bắt đầu tìm nguồn cung gỗ từ các khu rừng trong nước."
            }
        },
        "stationery": {
            "definition_vi": "văn phòng phẩm (đặc biệt là giấy viết thư, phong bì)",
            "examples_vi": [
                "Chúng ta không còn đủ giấy tờ văn phòng phẩm nữa, vì vậy làm ơn hãy đặt mua thêm.",
                "Bộ giấy tiêu đề mới có in biểu trưng của công ty bằng mực xanh ở đầu trang."
            ],
            "collocations": [
                "office stationery",
                "stationery supplies",
                "stationery store",
                "personalized stationery"
            ],
            "usage": {
                "structures": [
                    "order/supply stationery (đặt mua / cung cấp văn phòng phẩm)"
                ],
                "prepositions": ["on"],
                "collocations": [
                    "company stationery",
                    "letterhead stationery",
                    "stationery cabinet",
                    "stationery department"
                ],
                "tip": "Mẹo nhớ chính tả tránh nhầm lẫn: 'stationEry' có chữ E (Envelopes / pEn = văn phòng phẩm, danh từ không đếm được), còn 'stationAry' có chữ A (stAnd = đứng yên, tính từ)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "stationery",
                    "example": "All official correspondence must be printed on company stationery.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "stationer",
                    "example": "We ordered custom-engraved invitations from a local stationer.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The administrative assistant ordered boxes of envelopes and matching _____ with the new corporate logo.",
                "answer": "stationery",
                "base_word": "stationery",
                "pos_hint": "danh từ không đếm được",
                "vi": "Trợ lý hành chính đã đặt mua nhiều hộp phong bì và giấy viết thư đồng bộ có in biểu trưng mới của công ty."
            }
        }
    },
    18: {
        "accurately": {
            "definition_vi": "một cách chính xác, chuẩn xác, không sai sót",
            "examples_vi": [
                "Để đánh giá chính xác những con số này, trước tiên chúng ta cần lấy một số dữ kiện từ bộ phận vận chuyển.",
                "Công ty tàu chở hàng container phải cân bằng tải trọng một cách chính xác nếu không có thể xảy ra thảm họa trên biển."
            ],
            "collocations": [
                "accurately reflect",
                "accurately estimate",
                "measure accurately",
                "accurately recorded"
            ],
            "usage": {
                "structures": [
                    "accurately + V / V + O + accurately (làm việc gì một cách chính xác)"
                ],
                "prepositions": [],
                "collocations": [
                    "accurately predict",
                    "accurately assess",
                    "accurate records",
                    "high degree of accuracy"
                ],
                "tip": "Trạng từ 'accurately' thường đứng ngay trước hoặc sau các động từ chỉ việc đo lường, dự đoán, phản ánh: 'reflect, estimate, predict, measure, record'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "inaccurate",
                    "example": "An inaccurate shipping address caused a three-day delivery delay.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Before sealing the crate, please check the packing slip to ensure the contents are listed with complete _____.",
                "answer": "accuracy",
                "base_word": "accurately",
                "pos_hint": "danh từ",
                "vi": "Trước khi niêm phong thùng hàng, vui lòng kiểm tra phiếu đóng gói để đảm bảo các món hàng bên trong được liệt kê với độ chính xác tuyệt đối."
            }
        },
        "carrier": {
            "definition_vi": "hãng vận chuyển, công ty giao nhận; hãng hàng không/viễn thông",
            "examples_vi": [
                "Lou, nhân viên vận chuyển yêu thích của chúng tôi, luôn đặc biệt cẩn thận với những chiếc hộp được đánh dấu \"dễ vỡ\" của chúng tôi.",
                "Ông Lau đã chuyển đổi hãng vận chuyển để tiết kiệm chi phí cho các đơn giao hàng ra ngoài tiểu bang."
            ],
            "collocations": [
                "shipping carrier",
                "freight carrier",
                "commercial carrier",
                "express carrier"
            ],
            "usage": {
                "structures": [
                    "via/by a commercial carrier (thông qua một hãng vận chuyển thương mại)"
                ],
                "prepositions": ["by", "via"],
                "collocations": [
                    "switch carriers",
                    "air carrier",
                    "mail carrier",
                    "overnight carrier"
                ],
                "tip": "Trong TOEIC, 'carrier' thường chỉ công ty vận tải/giao hàng (shipping carrier), hãng hàng không (air carrier), hoặc nhà mạng viễn thông (wireless carrier)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "carry",
                    "example": "Our hardware store carries a full line of electrical tools.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "carrier",
                    "example": "Packages shipped via our express carrier are guaranteed to arrive by noon.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "carriage",
                    "example": "The contract stipulates that carriage charges are paid by the buyer.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "International orders are dispatched through a reliable global freight _____.",
                "answer": "carrier",
                "base_word": "carrier",
                "pos_hint": "danh từ chỉ hãng vận chuyển",
                "vi": "Các đơn đặt hàng quốc tế được gửi đi thông qua một hãng vận tải hàng hóa toàn cầu đáng tin cậy."
            }
        },
        "catalog": {
            "definition_vi": "(n) cuốn danh mục sản phẩm (ca-ta-lô); (v) lập danh mục, phân loại",
            "examples_vi": [
                "Cuốn danh mục sản phẩm mùa thu sắp tới giới thiệu một số mặt hàng từ Lào mà trước đây ông Lau chưa từng có khả năng cung cấp.",
                "Ellen đã phân loại các khiếu nại vào danh mục theo mức độ nghiêm trọng."
            ],
            "collocations": [
                "product catalog",
                "mail-order catalog",
                "online catalog",
                "catalog items"
            ],
            "usage": {
                "structures": [
                    "browse/request a catalog (xem / yêu cầu cuốn danh mục sản phẩm)",
                    "catalog + O (lập danh mục / phân loại cái gì)"
                ],
                "prepositions": ["in", "from", "by"],
                "collocations": [
                    "seasonal catalog",
                    "latest catalog",
                    "order from a catalog",
                    "digital cataloging"
                ],
                "tip": "Có thể viết là 'catalog' (tiếng Anh Mỹ) hoặc 'catalogue' (tiếng Anh Anh); vừa là danh từ vừa là ngoại động từ."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "catalog",
                    "example": "The archivist spent three months cataloging the museum's new acquisitions.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "catalog",
                    "example": "You can view our complete spring catalog on our website.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "cataloged",
                    "example": "All cataloged spare parts are stored in the north warehouse.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The museum's newly acquired artifacts are being _____ by a team of historians before going on display.",
                "answer": "cataloged",
                "base_word": "catalog",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed) ở câu bị động",
                "vi": "Các hiện vật mới thu thập được của bảo tàng đang được một nhóm các nhà sử học lập danh mục trước khi đưa ra trưng bày."
            }
        },
        "fulfill": {
            "definition_vi": "hoàn thành, đáp ứng (yêu cầu/đơn hàng), thực hiện (nghĩa vụ/lời hứa)",
            "examples_vi": [
                "Các kỹ sư đã đáp ứng yêu cầu của khách hàng về những màn hình hiển thị lớn hơn.",
                "Kỳ vọng của bà ấy cao đến mức chúng tôi biết rằng sẽ rất khó để đáp ứng được."
            ],
            "collocations": [
                "fulfill an order",
                "fulfill a requirement",
                "fulfill a contract",
                "order fulfillment"
            ],
            "usage": {
                "structures": [
                    "fulfill + an order/request/requirement/obligation/promise (thực hiện đơn hàng / đáp ứng yêu cầu / hoàn thành nghĩa vụ)"
                ],
                "prepositions": ["by"],
                "collocations": [
                    "fulfill expectations",
                    "fulfillment center",
                    "fulfilling career",
                    "fail to fulfill"
                ],
                "tip": "Trong thương mại điện tử và vận chuyển (Shipping), 'order fulfillment / fulfillment center' có nghĩa là việc xử lý & hoàn tất đơn hàng / trung tâm hoàn tất đơn hàng."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "fulfilled",
                    "example": "All fulfilled orders are scanned before leaving the loading dock.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To speed up delivery times, the online retailer opened a new regional _____ center in Ohio.",
                "answer": "fulfillment",
                "base_word": "fulfill",
                "pos_hint": "danh từ bổ nghĩa",
                "vi": "Để rút ngắn thời gian giao hàng, nhà bán lẻ trực tuyến đã mở một trung tâm xử lý đơn hàng khu vực mới tại Ohio."
            }
        },
        "integral": {
            "definition_vi": "thiết yếu, không thể tách rời, tối quan trọng",
            "examples_vi": [
                "Quan hệ khách hàng tốt là một yếu tố thiết yếu không thể tách rời của bất kỳ doanh nghiệp nào.",
                "Nguồn hàng tồn kho ổn định đáng tin cậy là yếu tố thiết yếu để việc giao các đơn hàng được tin cậy."
            ],
            "collocations": [
                "an integral part of",
                "an integral component",
                "integral to success",
                "play an integral role"
            ],
            "usage": {
                "structures": [
                    "be integral to + N (thiết yếu đối với cái gì)",
                    "an integral part/component of + N (một phần không thể tách rời của cái gì)"
                ],
                "prepositions": ["to", "of"],
                "collocations": [
                    "integral member of the team",
                    "integral element",
                    "seamless integration",
                    "integrate into"
                ],
                "tip": "Gần như luôn xuất hiện trong 2 cấu trúc cố định: 'an integral part of' hoặc 'be integral to + cụm danh từ'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "integrally",
                    "example": "Quality control is integrally linked to customer satisfaction.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new software allows seamless _____ of our warehouse tracking and billing systems.",
                "answer": "integration",
                "base_word": "integral",
                "pos_hint": "danh từ",
                "vi": "Phần mềm mới cho phép tích hợp liền mạch hệ thống theo dõi kho hàng và hệ thống thanh toán của chúng tôi."
            }
        },
        "inventory": {
            "definition_vi": "(n) hàng tồn kho, bảng kiểm kê hàng hóa; (v) kiểm kê kho",
            "examples_vi": [
                "Cửa hàng đóng cửa một ngày trong năm để nhân viên có thể kiểm kê hàng hóa trong kho.",
                "Lượng hàng hóa lưu kho của họ không thay đổi nhiều qua các năm."
            ],
            "collocations": [
                "take inventory",
                "manage inventory",
                "inventory control",
                "excess inventory"
            ],
            "usage": {
                "structures": [
                    "take/conduct (an) inventory of + N (tiến hành kiểm kê kho hàng)",
                    "keep/have in inventory (có lưu trong kho)"
                ],
                "prepositions": ["of", "in"],
                "collocations": [
                    "annual inventory",
                    "inventory management system",
                    "liquidate inventory",
                    "inventory levels"
                ],
                "tip": "Cụm cố định bắt buộc phải nhớ cho TOEIC: 'take inventory' (kiểm kê hàng tồn kho)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "inventory",
                    "example": "Warehouse clerks inventory all incoming shipments every evening.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "inventory",
                    "example": "Our computerized system tracks inventory across twelve retail locations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "inventoried",
                    "example": "All inventoried items are tagged with a barcode sticker.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The hardware store will close early on Sunday so staff can take _____ of the stockroom.",
                "answer": "inventory",
                "base_word": "inventory",
                "pos_hint": "danh từ trong cụm take inventory",
                "vi": "Cửa hàng dụng cụ sẽ đóng cửa sớm vào Chủ nhật để nhân viên có thể kiểm kê kho hàng."
            }
        },
        "minimize": {
            "definition_vi": "giảm thiểu tối đa",
            "examples_vi": [
                "Nhân viên vận chuyển đã giảm thiểu khiếu nại của khách hàng bằng cách làm thêm giờ để giao các kiện hàng nhanh chóng.",
                "Để giữ cho khách hàng hài lòng và giảm thiểu tác động của cuộc đình công từ hãng vận chuyển, chúng tôi đã gửi đơn hàng trực tiếp cho họ."
            ],
            "collocations": [
                "minimize costs",
                "minimize risk",
                "minimize delays",
                "minimize waste"
            ],
            "usage": {
                "structures": [
                    "minimize + O (damage/risk/delays/disruption/costs) (giảm thiểu thiệt hại/rủi ro/chậm trễ/gián đoạn/chi phí)"
                ],
                "prepositions": [],
                "collocations": [
                    "minimize inconvenience to customers",
                    "minimal impact",
                    "keep costs to a minimum",
                    "at a minimum"
                ],
                "tip": "Trái nghĩa với 'maximize'; rất hay xuất hiện trong thông báo xin lỗi khách hàng: 'to minimize inconvenience to our patrons' (để giảm thiểu sự bất tiện cho khách hàng)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "minimally",
                    "example": "Production was only minimally affected by the brief power outage.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Thanks to the protective foam packaging, the fragile glassware suffered only _____ damage in transit.",
                "answer": "minimal",
                "base_word": "minimize",
                "pos_hint": "tính từ",
                "vi": "Nhờ lớp bao bì xốp bảo vệ, đồ thủy tinh dễ vỡ chỉ bị hư hại ở mức tối thiểu trong quá trình vận chuyển."
            }
        },
        "on hand": {
            "definition_vi": "có sẵn (trong kho); có mặt sẵn sàng (để hỗ trợ)",
            "examples_vi": [
                "Chúng tôi có quá nhiều hàng tồn kho sẵn có, vì vậy chúng tôi đã tổ chức một đợt giảm giá mùa hè.",
                "Nhân viên mới sẽ có mặt sẵn sàng nếu chúng ta cần thêm sự trợ giúp trong việc gửi các đơn hàng."
            ],
            "collocations": [
                "have on hand",
                "stock on hand",
                "cash on hand",
                "be on hand to assist"
            ],
            "usage": {
                "structures": [
                    "have + sth + on hand (có sẵn cái gì để dùng ngay)",
                    "be on hand + to V (có mặt sẵn sàng tại chỗ để làm gì)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "keep spare parts on hand",
                    "staff on hand",
                    "supplies on hand",
                    "sufficient inventory on hand"
                ],
                "tip": "Dùng cho cả vật ('keep extra supplies on hand' = dự trữ sẵn vật tư) và người ('technicians will be on hand to answer questions' = kỹ thuật viên sẽ có mặt sẵn để trả lời câu hỏi)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "hand",
                    "example": "Please hand your completed customs form to the agent at the gate.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "hand",
                    "example": "All fragile parcels are inspected by hand before shipping.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "handy",
                    "example": "Keep your tracking number handy in case you need to check your delivery status.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "handily",
                    "example": "The compact label printer fits handily on any shipping desk.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Customer service representatives will be _____ throughout the conference to assist with registration.",
                "answer": "on hand",
                "base_word": "on hand",
                "pos_hint": "cụm tính từ chỉ sự có mặt sẵn sàng",
                "vi": "Các nhân viên đại diện chăm sóc khách hàng sẽ có mặt sẵn sàng trong suốt hội nghị để hỗ trợ việc đăng ký."
            }
        },
        "remember": {
            "definition_vi": "nhớ, ghi nhớ",
            "examples_vi": [
                "Tôi đã nhớ ra tên của nhân viên giao hàng ngay khi vừa cúp máy.",
                "Tôi sẽ nhớ mã số két sắt mà không cần phải ghi chép lại."
            ],
            "collocations": [
                "remember to include",
                "remember doing something",
                "clearly remember",
                "please remember that"
            ],
            "usage": {
                "structures": [
                    "remember + to V (nhớ phải làm gì - nhiệm vụ chưa làm)",
                    "remember + V-ing (nhớ là đã làm gì trong quá khứ)"
                ],
                "prepositions": ["for", "as"],
                "collocations": [
                    "remember the deadline",
                    "worth remembering",
                    "hard to remember",
                    "in remembrance of"
                ],
                "tip": "Cấu trúc kinh điển: 'remember + to V' (nhớ phải làm việc gì: Please remember to attach the shipping label) khác với 'remember + V-ing' (nhớ đã làm gì)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "remember",
                    "example": "Please remember to sign the delivery confirmation receipt.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "remembrance",
                    "example": "A plaque was placed in the lobby in remembrance of the company's founder.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "memorable",
                    "example": "The gala dinner was a memorable conclusion to the annual trade convention.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Warehouse staff must remember _____ the loading bay doors before leaving at night.",
                "answer": "to lock",
                "base_word": "remember",
                "pos_hint": "động từ nguyên mẫu có to (to V) sau remember chỉ nhiệm vụ",
                "vi": "Nhân viên kho phải nhớ khóa cửa khu vực bốc dỡ hàng trước khi ra về vào buổi tối."
            }
        },
        "ship": {
            "definition_vi": "(v) vận chuyển, gửi hàng; (n) tàu thủy",
            "examples_vi": [
                "Eva đã đóng gói và gửi kiện hàng một cách cẩn thận vì cô biết đồ bên trong làm bằng thủy tinh.",
                "Rất ít khách hàng nghĩ đến việc kiện hàng của họ sẽ được vận chuyển như thế nào, và hiếm khi có mặt ở nhà khi kiện hàng tới nơi."
            ],
            "collocations": [
                "ship an order",
                "ship overnight",
                "free shipping",
                "incoming shipment"
            ],
            "usage": {
                "structures": [
                    "ship + sth + to + sb/place (gửi/vận chuyển hàng đến ai/nơi nào)",
                    "ship + by air/sea/rail (vận chuyển bằng đường hàng không/biển/sắt)"
                ],
                "prepositions": ["to", "from", "by", "via"],
                "collocations": [
                    "shipping and handling",
                    "shipping department",
                    "delay a shipment",
                    "drop shipping"
                ],
                "tip": "Phân biệt 3 danh từ: 'shipment' (lô hàng được gửi / việc gửi hàng), 'shipping' (dịch vụ/phí vận chuyển: free shipping), và 'shipper' (người/công ty gửi hàng)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "shipping",
                    "example": "Orders over one hundred dollars qualify for complimentary express shipping.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The _____ of electronic components from Taiwan was delayed by two days due to severe weather.",
                "answer": "shipment",
                "base_word": "ship",
                "pos_hint": "danh từ chỉ lô hàng",
                "vi": "Lô hàng linh kiện điện tử từ Đài Loan đã bị trễ hai ngày do thời tiết xấu."
            }
        },
        "sufficiently": {
            "definition_vi": "đủ, một cách đầy đủ",
            "examples_vi": [
                "Toa tàu chở hàng đã bị hư hỏng nặng đến mức không thể chất hàng lên xe tải được.",
                "Chúng tôi đã sắp xếp tổ chức đầy đủ để bắt đầu chuyển các kiện hàng pallet vào ngày mai."
            ],
            "collocations": [
                "sufficiently prepared",
                "sufficiently protected",
                "sufficiently large",
                "sufficient funds"
            ],
            "usage": {
                "structures": [
                    "sufficiently + adj/adv (+ to V) (đủ... để làm gì)",
                    "be sufficient for + N / to V (đủ cho cái gì / để làm gì)"
                ],
                "prepositions": ["for", "to"],
                "collocations": [
                    "sufficient time",
                    "sufficient inventory",
                    "self-sufficient",
                    "sufficiently padded"
                ],
                "tip": "Ngược lại với 'enough' (đứng SAU tính từ: large enough), trạng từ 'sufficiently' luôn đứng TRƯỚC tính từ hoặc phân từ (sufficiently large / sufficiently trained)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "sufficiency",
                    "example": "The audit confirmed the sufficiency of the bank's cash reserves.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "insufficient",
                    "example": "The order could not be processed due to insufficient stock in the warehouse.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Please ensure that all fragile items are _____ wrapped in bubble wrap before sealing the box.",
                "answer": "sufficiently",
                "base_word": "sufficiently",
                "pos_hint": "trạng từ",
                "vi": "Vui lòng đảm bảo rằng tất cả các mặt hàng dễ vỡ đều được bọc đủ kỹ bằng màng xốp hơi trước khi dán kín thùng."
            }
        },
        "supply": {
            "definition_vi": "(n) nguồn cung, vật tư dự trữ; (v) cung cấp, tiếp tế",
            "examples_vi": [
                "Bằng cách tận dụng tốt hơn nguồn vật tư của mình, chúng ta có thể tránh phải đặt hàng cho đến tháng sau.",
                "Gerald đã cung cấp cho nhân viên bộ phận vận chuyển đủ nhãn dán để dùng trong cả một năm."
            ],
            "collocations": [
                "office supplies",
                "supply and demand",
                "supply chain",
                "in short supply"
            ],
            "usage": {
                "structures": [
                    "supply + sb + with + sth (cung cấp cho ai cái gì)",
                    "supply + sth + to + sb (cung cấp cái gì cho ai)"
                ],
                "prepositions": ["with", "to", "in"],
                "collocations": [
                    "medical supplies",
                    "steady supply",
                    "leading supplier",
                    "exhaust the supply"
                ],
                "tip": "Danh từ số nhiều 'supplies' nghĩa là 'vật tư, nhu yếu phẩm' (office/medical/cleaning supplies); danh từ chỉ người/công ty cung ứng là 'supplier'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "supply",
                    "example": "Our company supplies packaging materials to over fifty factories.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "supplier",
                    "example": "We are negotiating with a new supplier to lower our raw material costs.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "supplies",
                    "example": "Please check the cabinet before ordering additional cleaning supplies.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The procurement manager is meeting with several potential _____ to compare wholesale prices.",
                "answer": "suppliers",
                "base_word": "supply",
                "pos_hint": "danh từ chỉ nhà cung cấp số nhiều",
                "vi": "Trưởng phòng thu mua đang gặp gỡ một số nhà cung cấp tiềm năng để so sánh giá bán buôn."
            }
        }
    },
    19: {
        "charge": {
            "definition_vi": "(v) tính phí, thu tiền; (n) chi phí, khoản phí; sự phụ trách",
            "examples_vi": [
                "Nhân viên đại diện chăm sóc khách hàng chịu trách nhiệm thông báo cho tất cả các khách hàng hiện tại rằng mức giá cao hơn sẽ được áp dụng vào tháng tới.",
                "Khoản phí phụ thu cho việc gói quà món hàng bạn mua sẽ hiển thị trên hóa đơn của bạn."
            ],
            "collocations": [
                "free of charge",
                "at no extra charge",
                "in charge of",
                "shipping charges"
            ],
            "usage": {
                "structures": [
                    "charge + (sb) + [số tiền] + for + sth (tính phí ai bao nhiêu tiền cho cái gì)",
                    "charge + sth + to + an account/credit card (ghi nợ khoản gì vào tài khoản/thẻ)",
                    "be in charge of + N (chịu trách nhiệm phụ trách cái gì)"
                ],
                "prepositions": ["for", "to", "of", "at"],
                "collocations": [
                    "service charge",
                    "admission charge",
                    "surcharge",
                    "overcharge a customer"
                ],
                "tip": "Ba cụm cố định xuất hiện liên tục trong TOEIC: 'free of charge' (miễn phí), 'at no additional charge' (không mất thêm phí), và 'in charge of' (phụ trách)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "charge",
                    "example": "The hotel does not charge guests for local telephone calls.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "charge",
                    "example": "A ten percent service charge is automatically added to group bills.",
                    "pos_source": "extended"
                },
                {
                    "pos": "verb",
                    "word": "overcharge",
                    "example": "The client called to complain that he had been overcharged on his monthly invoice.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "chargeable",
                    "example": "Any repairs not covered by the warranty will be chargeable to the owner.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Replacement parts will be provided free of _____ if the appliance fails within the warranty period.",
                "answer": "charge",
                "base_word": "charge",
                "pos_hint": "danh từ trong cụm free of charge",
                "vi": "Phụ tùng thay thế sẽ được cung cấp miễn phí nếu thiết bị gặp sự cố trong thời gian bảo hành."
            }
        },
        "compile": {
            "definition_vi": "biên soạn, tập hợp, tổng hợp (tài liệu, dữ liệu, danh sách)",
            "examples_vi": [
                "Tôi đã tổng hợp một danh sách các mặt hàng phổ biến nhất trong cuốn danh mục bán hàng của chúng ta.",
                "Nhân viên văn phòng chịu trách nhiệm tập hợp các đơn đặt hàng vào cuối ngày."
            ],
            "collocations": [
                "compile a list",
                "compile data",
                "compile a report",
                "compile statistics"
            ],
            "usage": {
                "structures": [
                    "compile + data/information/a list/a report + from + N (tổng hợp dữ liệu/danh sách/báo cáo từ nhiều nguồn)"
                ],
                "prepositions": ["from", "into"],
                "collocations": [
                    "compile a directory",
                    "compile survey results",
                    "newly compiled figures",
                    "data compilation"
                ],
                "tip": "Thường đi với các tân ngữ chỉ dữ liệu hoặc tài liệu được thu thập từ nhiều nguồn: 'compile a report / list / directory / statistics / data'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "compiler",
                    "example": "The compiler of the annual industry directory verified every company address.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The market research team spent six weeks _____ data on consumer spending habits.",
                "answer": "compiling",
                "base_word": "compile",
                "pos_hint": "danh động từ (V-ing) sau spend time",
                "vi": "Nhóm nghiên cứu thị trường đã dành sáu tuần để tổng hợp dữ liệu về thói quen chi tiêu của người tiêu dùng."
            }
        },
        "customer": {
            "definition_vi": "khách hàng (người mua hàng hóa hoặc dịch vụ)",
            "examples_vi": [
                "Chúng ta hãy đảm bảo tất cả các hóa đơn gửi cho khách hàng được lưu giữ theo thứ tự bảng chữ cái.",
                "Như một phần trong kế hoạch làm hài lòng khách hàng của chúng ta, hãy chiết khấu cho những khách hàng thanh toán hóa đơn trong vòng một tuần."
            ],
            "collocations": [
                "customer service",
                "customer satisfaction",
                "regular customer",
                "prospective customer"
            ],
            "usage": {
                "structures": [
                    "customer + N (danh từ ghép: customer service/support/satisfaction/loyalty/base)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "valued customer",
                    "loyal customer",
                    "customer base",
                    "attract new customers"
                ],
                "tip": "Họ từ liên quan cần chú ý trong TOEIC: 'custom' (phong tục / hải quan / đặt làm riêng), 'customs' (thuế/cơ quan hải quan), và 'customize' (tùy chỉnh theo yêu cầu khách hàng)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "customize",
                    "example": "We can customize the billing software to meet your accounting department's needs.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "customer",
                    "example": "Every customer receives an automated e-mail receipt after payment.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "customizable",
                    "example": "The enterprise platform features fully customizable invoice templates.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "customary",
                    "example": "It is customary in this industry to offer a discount for early payment.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Our software engineers can _____ the dashboard layout according to each client's preferences.",
                "answer": "customize",
                "base_word": "customer",
                "pos_hint": "động từ nguyên mẫu (tùy chỉnh)",
                "vi": "Các kỹ sư phần mềm của chúng tôi có thể tùy chỉnh bố cục bảng điều khiển theo sở thích của từng khách hàng."
            }
        },
        "discount": {
            "definition_vi": "(n) khoản giảm giá, sự chiết khấu; (v) giảm giá, chiết khấu",
            "examples_vi": [
                "Chúng tôi đang áp dụng mức giảm giá 10 phần trăm cho tất cả các khách hàng mới.",
                "Họ đã giảm giá đối với những hàng hóa bị hư hỏng trong quá trình vận chuyển."
            ],
            "collocations": [
                "offer a discount",
                "at a discount",
                "bulk discount",
                "employee discount"
            ],
            "usage": {
                "structures": [
                    "a discount on + N (giảm giá cho mặt hàng gì)",
                    "at a discount (với mức giá đã giảm)",
                    "discount + O (giảm giá mặt hàng gì)"
                ],
                "prepositions": ["on", "at", "off"],
                "collocations": [
                    "steep discount",
                    "ten percent discount",
                    "discounted price",
                    "discount coupon"
                ],
                "tip": "Chú ý giới từ: 'a discount ON + mặt hàng' (a 15% discount on all office furniture) và 'AT a discount' (bán với giá chiết khấu)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "discount",
                    "example": "The bookstore discounts all hardcover bestsellers by twenty percent.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "discount",
                    "example": "Members receive an exclusive discount on conference registration fees.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "discounted",
                    "example": "Discounted tickets are available for groups of ten or more.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Subscribers who renew their memberships before December 31 will receive a _____ rate.",
                "answer": "discounted",
                "base_word": "discount",
                "pos_hint": "tính từ (V-ed) bổ nghĩa cho rate",
                "vi": "Những người đăng ký gia hạn tư cách thành viên trước ngày 31 tháng 12 sẽ nhận được mức giá ưu đãi giảm giá."
            }
        },
        "efficient": {
            "definition_vi": "hiệu quả, năng suất cao (ít tốn thời gian, công sức hoặc chi phí)",
            "examples_vi": [
                "Nhân viên kế toán xử lý các biên lai của khách hàng hiệu quả đến mức cô đã hoàn thành công việc trước bữa trưa.",
                "Việc lập hóa đơn điện tử đã giúp chúng tôi làm việc hiệu quả."
            ],
            "collocations": [
                "cost-efficient",
                "fuel-efficient",
                "energy-efficient",
                "work efficiently"
            ],
            "usage": {
                "structures": [
                    "be efficient in/at + V-ing (hiệu quả trong việc làm gì)",
                    "energy-efficient / cost-efficient (tiết kiệm năng lượng / tối ưu chi phí)"
                ],
                "prepositions": ["in", "at"],
                "collocations": [
                    "highly efficient system",
                    "improve operational efficiency",
                    "process orders efficiently",
                    "efficient use of resources"
                ],
                "tip": "Phân biệt 'effective' (hiệu quả = đạt được kết quả mong muốn) và 'efficient' (hiệu suất cao = làm nhanh, tiết kiệm thời gian/chi phí/năng lượng)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "inefficient",
                    "example": "The old manual filing system was slow and inefficient.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Automating the billing process has enabled the accounting staff to handle invoices much more _____.",
                "answer": "efficiently",
                "base_word": "efficient",
                "pos_hint": "trạng từ",
                "vi": "Việc tự động hóa quy trình lập hóa đơn đã giúp nhân viên kế toán xử lý hóa đơn hiệu quả hơn rất nhiều."
            }
        },
        "estimate": {
            "definition_vi": "(v) ước tính, định giá sơ bộ; (n) bản ước tính, bảng báo giá ước lượng",
            "examples_vi": [
                "Chúng tôi ước tính khoản thua lỗ trong năm nay vào khoảng năm nghìn đô la.",
                "Theo đánh giá của người chủ, mức độ hài lòng cao của khách hàng là thước đo thỏa đáng cho thấy công ty đang hoạt động tốt ra sao."
            ],
            "collocations": [
                "cost estimate",
                "rough estimate",
                "estimate at",
                "written estimate"
            ],
            "usage": {
                "structures": [
                    "estimate + sth + at + [con số/số tiền] (ước tính cái gì ở mức bao nhiêu)",
                    "provide a free estimate (cung cấp bảng báo giá ước tính miễn phí)"
                ],
                "prepositions": ["at", "for"],
                "collocations": [
                    "conservative estimate",
                    "preliminary estimate",
                    "estimated time of arrival",
                    "repair estimate"
                ],
                "tip": "Trong TOEIC, 'an estimate' là danh từ đếm được rất phổ biến chỉ 'bảng báo giá dự toán' mà nhà thầu/thợ sửa chữa đưa cho khách trước khi làm việc."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "estimated",
                    "example": "The estimated cost of the warehouse renovation is two hundred thousand dollars.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The contractor provided a detailed written _____ of the materials and labor required for the roof repair.",
                "answer": "estimate",
                "base_word": "estimate",
                "pos_hint": "danh từ chỉ bảng báo giá dự toán",
                "vi": "Nhà thầu đã cung cấp một bản dự toán chi tiết bằng văn bản về vật liệu và nhân công cần thiết để sửa mái nhà."
            }
        },
        "impose": {
            "definition_vi": "áp đặt (thuế, phí phạt, quy định); gây phiền hà",
            "examples_vi": [
                "Công ty sẽ áp dụng một khoản phụ phí đối với bất kỳ mặt hàng nào bị trả lại.",
                "Chúng ta không nên áp đặt gánh nặng lên nhân viên bằng cách yêu cầu họ làm việc vào cuối tuần."
            ],
            "collocations": [
                "impose a fine",
                "impose a tax",
                "impose a surcharge",
                "impose restrictions"
            ],
            "usage": {
                "structures": [
                    "impose + A (a tax/fine/fee/ban/limit) + on/upon + B (áp đặt thuế/phạt/phí/lệnh cấm lên ai/cái gì)",
                    "impose on/upon + sb (làm phiền / ép buộc ai)"
                ],
                "prepositions": ["on", "upon"],
                "collocations": [
                    "impose a penalty",
                    "impose strict regulations",
                    "impose tariffs on imports",
                    "newly imposed rules"
                ],
                "tip": "Luôn đi kèm giới từ 'on' hoặc 'upon' và các tân ngữ chỉ khoản phạt, thuế, phí hoặc hạn chế (impose a fee/fine/tax/penalty/restriction on...)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "imposed",
                    "example": "Government-imposed safety standards must be met by all manufacturers.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "A five percent late fee will be _____ on all invoices that remain unpaid after thirty days.",
                "answer": "imposed",
                "base_word": "impose",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed) ở câu bị động",
                "vi": "Một khoản phí trả chậm năm phần trăm sẽ được áp dụng cho tất cả các hóa đơn chưa thanh toán sau ba mươi ngày."
            }
        },
        "mistake": {
            "definition_vi": "(n) lỗi, sai lầm, sự nhầm lẫn; (v) nhầm lẫn",
            "examples_vi": [
                "Tôi đã mắc một sai sót khi cộng hóa đơn của quý khách và chúng tôi đã tính thừa của quý khách hai mươi đô la.",
                "Thật là một sai lầm khi nghĩ rằng sếp của tôi sẽ biết điều khi tôi giải thích hoàn cảnh của mình cho ông ấy."
            ],
            "collocations": [
                "make a mistake",
                "by mistake",
                "billing mistake",
                "mistake A for B"
            ],
            "usage": {
                "structures": [
                    "make a mistake (mắc lỗi)",
                    "by mistake (do nhầm lẫn / vô tình)",
                    "mistake + A + for + B (nhầm A với B)"
                ],
                "prepositions": ["by", "in", "for", "about"],
                "collocations": [
                    "common mistake",
                    "costly mistake",
                    "correct a mistake",
                    "mistaken identity"
                ],
                "tip": "Nhớ cụm giới từ 'by mistake' (do nhầm lẫn, đồng nghĩa với accidentally / inadvertently) và tính từ 'mistaken' (hiểu nhầm: be mistaken about sth)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "mistakenly",
                    "example": "The accounting clerk mistakenly sent the invoice to the wrong client.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Your credit card was _____ billed twice for the same transaction, and a refund has already been issued.",
                "answer": "mistakenly",
                "base_word": "mistake",
                "pos_hint": "trạng từ",
                "vi": "Thẻ tín dụng của quý khách đã bị tính tiền nhầm hai lần cho cùng một giao dịch và khoản hoàn tiền đã được thực hiện."
            }
        },
        "order": {
            "definition_vi": "(n) đơn đặt hàng; mệnh lệnh; thứ tự; (v) đặt hàng; ra lệnh",
            "examples_vi": [
                "Khách hàng đã đặt một đơn hàng mua mười chiếc ghế mới.",
                "Chúng tôi được lệnh phải kiểm kê kho ngay lập tức để có thể giải trình về những món đồ bị thất lạc."
            ],
            "collocations": [
                "place an order",
                "fill an order",
                "out of order",
                "in order to"
            ],
            "usage": {
                "structures": [
                    "place/cancel/fill/process an order for + N (đặt/hủy/thực hiện/xử lý đơn hàng mua cái gì)",
                    "out of order (bị hỏng - dùng cho máy móc)"
                ],
                "prepositions": ["for", "on", "in", "out of"],
                "collocations": [
                    "purchase order",
                    "back order",
                    "bulk order",
                    "in alphabetical order"
                ],
                "tip": "Nằm lòng các cụm từ với 'order' trong TOEIC: 'place an order' (đặt hàng), 'on order' (đã đặt nhưng chưa về), 'on back order' (tạm hết hàng chờ nhập), và 'out of order' (máy hỏng)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "order",
                    "example": "You can order replacement ink cartridges directly from our website.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "order",
                    "example": "Please quote your order number when inquiring about a delivery.",
                    "pos_source": "extended"
                },
                {
                    "pos": "verb",
                    "word": "reorder",
                    "example": "The system automatically reorders items when stock falls below fifty units.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "orderly",
                    "example": "Please exit the building in a calm and orderly manner during the fire drill.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Customers who place an _____ before 3:00 P.M. will receive next-day delivery.",
                "answer": "order",
                "base_word": "order",
                "pos_hint": "danh từ trong cụm place an order",
                "vi": "Những khách hàng đặt hàng trước 3 giờ chiều sẽ nhận được hàng giao vào ngày hôm sau."
            }
        },
        "promptly": {
            "definition_vi": "ngay lập tức, nhanh chóng; đúng giờ",
            "examples_vi": [
                "Chúng tôi luôn trả lời thư của khách hàng một cách nhanh chóng.",
                "Nhân viên bán hàng mới đã nhanh chóng đề nghị hoàn tiền đầy đủ cho số hàng hóa bị hư hỏng."
            ],
            "collocations": [
                "reply promptly",
                "pay promptly",
                "promptly at 9:00",
                "prompt service"
            ],
            "usage": {
                "structures": [
                    "respond/reply/pay/act + promptly (phản hồi/thanh toán/hành động ngay lập tức)",
                    "promptly at + [giờ] (đúng vào lúc mấy giờ)"
                ],
                "prepositions": ["at", "to"],
                "collocations": [
                    "prompt payment",
                    "prompt attention",
                    "handle complaints promptly",
                    "prompt delivery"
                ],
                "tip": "'Promptly' vừa mang nghĩa 'ngay lập tức' (reply promptly) vừa mang nghĩa 'đúng giờ' khi đứng trước mốc thời gian (The meeting starts promptly at 9:00 A.M.)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "promptly",
                    "example": "All billing inquiries are addressed promptly by our accounting team.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "We appreciate your _____ payment of the enclosed invoice within fifteen days.",
                "answer": "prompt",
                "base_word": "promptly",
                "pos_hint": "tính từ bổ nghĩa cho payment",
                "vi": "Chúng tôi trân trọng việc quý khách thanh toán nhanh chóng hóa đơn đính kèm trong vòng mười lăm ngày."
            }
        },
        "rectify": {
            "definition_vi": "sửa chữa, khắc phục (sai sót, sự cố, tình hình)",
            "examples_vi": [
                "Anh ấy đã khắc phục vấn đề bằng cách hoàn lại tiền tích lũy cho khách hàng đối với những món đồ chưa sử dụng mà cô trả lại.",
                "Xấu hổ vì hành vi của mình, anh ấy đã sửa chữa tình hình bằng cách viết một bức thư xin lỗi."
            ],
            "collocations": [
                "rectify an error",
                "rectify a mistake",
                "rectify the situation",
                "rectify a problem"
            ],
            "usage": {
                "structures": [
                    "rectify + an error/mistake/problem/omission/discrepancy (khắc phục lỗi/sai sót/vấn đề/sự chênh lệch)"
                ],
                "prepositions": ["by"],
                "collocations": [
                    "rectify a billing error",
                    "take steps to rectify",
                    "immediately rectify",
                    "rectify an oversight"
                ],
                "tip": "Từ trang trọng đồng nghĩa với 'correct / fix / remedy', rất hay gặp trong thư xin lỗi khách hàng về lỗi hóa đơn (rectify the billing error)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "rectify",
                    "example": "The payroll department promised to rectify the underpayment on Friday's check.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "rectification",
                    "example": "Prompt rectification of invoice errors helps maintain client trust.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "rectifiable",
                    "example": "Fortunately, the software glitch was easily rectifiable.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Once the accounting discrepancy was discovered, the manager took immediate action to _____ it.",
                "answer": "rectify",
                "base_word": "rectify",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Ngay khi phát hiện ra sự chênh lệch kế toán, người quản lý đã có hành động ngay lập tức để khắc phục nó."
            }
        },
        "terms": {
            "definition_vi": "các điều khoản, điều kiện (trong hợp đồng, thanh toán)",
            "examples_vi": [
                "Các điều khoản thanh toán đã được liệt kê rõ ràng ở cuối hóa đơn.",
                "Các điều khoản của thỏa thuận yêu cầu các mặt hàng phải được thanh toán đầy đủ trước khi được vận chuyển đi."
            ],
            "collocations": [
                "terms of payment",
                "terms and conditions",
                "under the terms of",
                "favorable terms"
            ],
            "usage": {
                "structures": [
                    "under the terms of + the contract/agreement (theo các điều khoản của hợp đồng/thỏa thuận)",
                    "terms of payment/service/delivery (điều khoản thanh toán/dịch vụ/giao hàng)"
                ],
                "prepositions": ["under", "of", "on"],
                "collocations": [
                    "negotiate terms",
                    "violate the terms",
                    "come to terms",
                    "in terms of"
                ],
                "tip": "Khi mang nghĩa 'điều khoản hợp đồng/thanh toán', danh từ này LUÔN ở dạng số nhiều 'terms' (under the terms of the agreement / terms and conditions)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "term",
                    "example": "The lease runs for an initial term of three years.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "terms",
                    "example": "Please read the terms and conditions carefully before signing.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "long-term",
                    "example": "We offer special credit terms to our long-term corporate partners.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Under the _____ of the service agreement, routine maintenance is provided at no additional cost.",
                "answer": "terms",
                "base_word": "terms",
                "pos_hint": "danh từ số nhiều chỉ điều khoản",
                "vi": "Theo các điều khoản của thỏa thuận dịch vụ, việc bảo trì định kỳ được cung cấp mà không tính thêm phí."
            }
        }
    },
    20: {
        "adjustment": {
            "definition_vi": "sự điều chỉnh, sự chỉnh sửa cho khớp",
            "examples_vi": [
                "Với những sự điều chỉnh này đối với số lượng ốc vít và đai ốc, chúng ta đã tiến gần đến việc có một con số kiểm đếm chính xác.",
                "Việc điều chỉnh số lượng các mặt hàng bị hư hỏng sẽ giúp chúng ta cân đối khớp các con số."
            ],
            "collocations": [
                "make an adjustment",
                "price adjustment",
                "inventory adjustment",
                "minor adjustment"
            ],
            "usage": {
                "structures": [
                    "make an adjustment to + N (thực hiện điều chỉnh đối với cái gì)",
                    "adjust to + N/V-ing (thích nghi với cái gì)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "cost-of-living adjustment",
                    "seasonal adjustment",
                    "adjustable height",
                    "adjust the figures"
                ],
                "tip": "Danh từ 'adjustment' luôn đi với giới từ 'to' (an adjustment to the invoice/inventory), còn tính từ 'adjustable' (có thể điều chỉnh được) rất hay dùng cho bàn ghế, kệ hàng."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "adjusted",
                    "example": "Please review the adjusted totals on the final inventory sheet.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The ergonomic office chair features _____ armrests and lumbar support.",
                "answer": "adjustable",
                "base_word": "adjustment",
                "pos_hint": "tính từ",
                "vi": "Chiếc ghế văn phòng công thái học có tay vịn và phần tựa lưng có thể điều chỉnh được."
            }
        },
        "automatically": {
            "definition_vi": "một cách tự động",
            "examples_vi": [
                "Chương trình sẽ tự động gửi thư điện tử phản hồi cho tất cả các tin nhắn trong thời gian cô ấy đi công tác xa.",
                "Cánh cửa mở ra một cách tự động."
            ],
            "collocations": [
                "automatically generated",
                "automatically updated",
                "automatically deducted",
                "automatically renew"
            ],
            "usage": {
                "structures": [
                    "automatically + V / be + automatically + V3/ed (tự động làm gì / được tự động làm gì)"
                ],
                "prepositions": [],
                "collocations": [
                    "shut off automatically",
                    "automatically enrolled",
                    "office automation",
                    "automatic renewal"
                ],
                "tip": "Trạng từ cực kỳ phổ biến trong TOEIC Part 5, thường đứng giữa 'be' và quá khứ phân từ (is automatically deducted/updated/renewed)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "automate",
                    "example": "The warehouse plans to automate its sorting and packing operations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "automated",
                    "example": "Customers receive an automated confirmation call the day before delivery.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Your annual magazine subscription will renew _____ unless you cancel it before the billing date.",
                "answer": "automatically",
                "base_word": "automatically",
                "pos_hint": "trạng từ",
                "vi": "Gói đăng ký tạp chí hàng năm của bạn sẽ tự động gia hạn trừ khi bạn hủy trước ngày lập hóa đơn."
            }
        },
        "crucial": {
            "definition_vi": "cốt yếu, tối quan trọng, mang tính quyết định",
            "examples_vi": [
                "Việc nắm được chúng ta có bao nhiêu sản phẩm trong kho là điều tối quan trọng đối với quy trình vận chuyển của chúng ta.",
                "Kiểm kê hàng tồn kho là một quy trình cốt yếu và phải được toàn thể nhân viên thực hiện nghiêm túc."
            ],
            "collocations": [
                "crucial role",
                "crucial to success",
                "crucial factor",
                "at a crucial stage"
            ],
            "usage": {
                "structures": [
                    "be crucial to/for + N (tối quan trọng đối với cái gì)",
                    "It is crucial that + S + (should) + V-inf (Điều cốt yếu là...)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "play a crucial part",
                    "crucial decision",
                    "crucial information",
                    "crucial importance"
                ],
                "tip": "Đồng nghĩa với 'vital, essential, critical, imperative'; đi với giới từ 'to' hoặc 'for' và cũng dùng trong cấu trúc giả định (It is crucial that...)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "cruciality",
                    "example": "The director emphasized the cruciality of accurate stock counts.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "crucial",
                    "example": "Timely delivery of raw materials is crucial to our production schedule.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "crucially",
                    "example": "Crucially, the new barcode system can operate even without an internet connection.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Accurate inventory tracking plays a _____ role in preventing stockouts during peak season.",
                "answer": "crucial",
                "base_word": "crucial",
                "pos_hint": "tính từ",
                "vi": "Việc theo dõi hàng tồn kho chính xác đóng vai trò tối quan trọng trong việc ngăn chặn tình trạng hết hàng vào mùa cao điểm."
            }
        },
        "discrepancy": {
            "definition_vi": "sự chênh lệch, sự khác biệt, sự không nhất quán (giữa các con số/báo cáo)",
            "examples_vi": [
                "Chúng tôi đã dễ dàng giải thích được sự chênh lệch giữa hai lần kiểm đếm.",
                "Trừ khi bạn phát hiện ra lỗi ngay lập tức, sự chênh lệch đó sẽ được nhập vào máy tính và trở nên rất khó sửa."
            ],
            "collocations": [
                "discrepancy between",
                "discrepancy in the figures",
                "resolve a discrepancy",
                "inventory discrepancy"
            ],
            "usage": {
                "structures": [
                    "a discrepancy between + A and B (sự chênh lệch giữa A và B)",
                    "a discrepancy in + N (sự sai lệch trong bảng số liệu/tài khoản)"
                ],
                "prepositions": ["between", "in"],
                "collocations": [
                    "minor discrepancy",
                    "investigate a discrepancy",
                    "explain the discrepancy",
                    "financial discrepancies"
                ],
                "tip": "Từ vựng TOEIC cấp độ 700+: luôn dùng để chỉ sự không khớp nhau giữa 2 con số, 2 bản kiểm kê hoặc hóa đơn với thực tế; đi kèm giới từ 'between' hoặc 'in'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "discrepancy",
                    "example": "The auditor found a discrepancy between the physical count and the digital log.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "discrepancies",
                    "example": "Any billing discrepancies must be reported within fourteen days of receipt.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "discrepant",
                    "example": "The two warehouses reported discrepant inventory figures for the same item.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The bookkeeper stayed late to reconcile several _____ between the bank statement and the ledger.",
                "answer": "discrepancies",
                "base_word": "discrepancy",
                "pos_hint": "danh từ số nhiều",
                "vi": "Nhân viên kế toán đã ở lại muộn để đối chiếu một số khoản chênh lệch giữa sao kê ngân hàng và sổ cái."
            }
        },
        "disturb": {
            "definition_vi": "làm phiền, quấy rầy; làm xáo trộn",
            "examples_vi": [
                "Hãy xem chúng ta có thể đếm trước được bao nhiêu sản phẩm trước kỳ kiểm kê để làm phiền ít khách hàng hơn.",
                "Tôi hy vọng mình không làm phiền bạn, nhưng tôi cần nhờ bạn dịch chuyển một chút để tôi có thể ghi chép các sản phẩm phía sau bạn."
            ],
            "collocations": [
                "do not disturb",
                "disturb customers",
                "sorry to disturb you",
                "cause a disturbance"
            ],
            "usage": {
                "structures": [
                    "without disturbing + O (mà không làm phiền đến ai)",
                    "cause a disturbance (gây ra sự xáo trộn/ồn ào)"
                ],
                "prepositions": ["by"],
                "collocations": [
                    "disturb the peace",
                    "disturbing trend",
                    "minimal disturbance",
                    "undisturbed"
                ],
                "tip": "Phân biệt: 'disturbance' (danh từ: sự xáo trộn/phiền phức), 'disturbed' (tính từ: bị làm phiền/lo lắng), và 'disturbing' (tính từ: đáng lo ngại, VD: a disturbing report)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "disturbing",
                    "example": "The audit revealed a disturbing rise in unexplained inventory losses.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Renovation work will be carried out at night to cause the least possible _____ to hotel guests.",
                "answer": "disturbance",
                "base_word": "disturb",
                "pos_hint": "danh từ",
                "vi": "Công việc cải tạo sẽ được thực hiện vào ban đêm để gây ra ít sự phiền hà nhất có thể cho khách nghỉ tại khách sạn."
            }
        },
        "liability": {
            "definition_vi": "trách nhiệm pháp lý; khoản nợ phải trả; mối bất lợi/gánh nặng",
            "examples_vi": [
                "Bảo hiểm trách nhiệm pháp lý của cửa hàng giúp bảo vệ trước tình trạng trộm cắp và hàng tồn kho bị hư hại.",
                "Những bậc cầu thang trơn trượt là một mối nguy trách nhiệm khủng khiếp đối với cửa hàng."
            ],
            "collocations": [
                "liability insurance",
                "accept liability",
                "assets and liabilities",
                "limited liability company"
            ],
            "usage": {
                "structures": [
                    "liability for + N (trách nhiệm pháp lý đối với cái gì)",
                    "assets and liabilities (tài sản và nợ phải trả)"
                ],
                "prepositions": ["for", "to"],
                "collocations": [
                    "assume liability",
                    "legal liability",
                    "tax liability",
                    "financial liabilities"
                ],
                "tip": "Trong kế toán TOEIC, số nhiều 'liabilities' là 'các khoản nợ phải trả' (trái nghĩa với 'assets' = tài sản); còn tính từ 'liable for/to' nghĩa là 'chịu trách nhiệm pháp lý / có nguy cơ bị'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "liability",
                    "example": "The shipping company disclaims all liability for unrecorded cash items.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "liable",
                    "example": "Tenants will be held liable for any damage caused to the property.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "liably",
                    "example": "Any contractor acting liably in breach of safety codes will be fined.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The parking garage management is not _____ for personal belongings left inside unattended vehicles.",
                "answer": "liable",
                "base_word": "liability",
                "pos_hint": "tính từ (chịu trách nhiệm pháp lý)",
                "vi": "Ban quản lý nhà để xe không chịu trách nhiệm pháp lý đối với đồ đạc cá nhân để lại bên trong các phương tiện không có người trông coi."
            }
        },
        "reflection": {
            "definition_vi": "hình ảnh phản chiếu; sự phản ánh; sự suy ngẫm",
            "examples_vi": [
                "Cô ấy nhìn thấy hình ảnh phản chiếu của mình trong gương.",
                "Ánh phản chiếu trên mặt kính khiến cô khó phân biệt được có bao nhiêu món đồ trên kệ."
            ],
            "collocations": [
                "a reflection of",
                "upon reflection",
                "accurate reflection",
                "reflect on"
            ],
            "usage": {
                "structures": [
                    "be a reflection of + N (là sự phản ánh của cái gì)",
                    "upon/on reflection (sau khi suy nghĩ/cân nhắc kỹ)",
                    "reflect + O (phản ánh chính xác số liệu/thực trạng)"
                ],
                "prepositions": ["of", "on", "upon"],
                "collocations": [
                    "reflect positively on",
                    "careful reflection",
                    "reflective vest",
                    "reflect changes"
                ],
                "tip": "Động từ 'reflect' xuất hiện rất nhiều trong ngữ cảnh hóa đơn và kiểm kê: 'The updated invoice reflects the 10% discount' (Hóa đơn cập nhật đã phản ánh khoản giảm giá 10%)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "reflective",
                    "example": "Warehouse workers must wear reflective safety vests on the loading dock.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Your monthly account statement may not yet _____ payments made within the last forty-eight hours.",
                "answer": "reflect",
                "base_word": "reflection",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Bản sao kê tài khoản hàng tháng của quý khách có thể chưa phản ánh các khoản thanh toán được thực hiện trong vòng bốn mươi tám giờ qua."
            }
        },
        "run": {
            "definition_vi": "(v) vận hành (máy móc), điều hành (doanh nghiệp), chạy (kiểm kê/chương trình); (n) đợt chạy",
            "examples_vi": [
                "Chừng nào máy tính còn đang chạy, bạn có thể tiếp tục thêm dữ liệu mới.",
                "Chúng ta sẽ tiến hành chạy kiểm kê kho vào cuối tuần tới, vì vậy đừng lên bất kỳ kế hoạch nào khác."
            ],
            "collocations": [
                "run a business",
                "run inventory",
                "run out of stock",
                "in the long run"
            ],
            "usage": {
                "structures": [
                    "run + a business/company/department (điều hành doanh nghiệp/phòng ban)",
                    "run + a machine/test/check/inventory (vận hành máy / chạy kiểm tra / kiểm kê)",
                    "run low on / run out of + N (sắp cạn / hết sạch cái gì)"
                ],
                "prepositions": ["out of", "on", "in"],
                "collocations": [
                    "run smoothly",
                    "run short of supplies",
                    "trial run",
                    "production run"
                ],
                "tip": "Trong chủ đề Inventory, nhớ kỹ 2 cụm 'run low on supplies' (sắp hết vật tư) và 'run out of stock' (hết sạch hàng trong kho)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "run",
                    "example": "She has been running the regional distribution center for five years.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "run",
                    "example": "The factory completed a test run of five hundred units.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "running",
                    "example": "The software maintains a running total of all items sold each day.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Please place an order for toner cartridges whenever the supply room _____ low.",
                "answer": "runs",
                "base_word": "run",
                "pos_hint": "động từ chia hiện tại đơn ngôi thứ 3 số ít",
                "vi": "Vui lòng đặt hàng hộp mực máy in bất cứ khi nào phòng vật tư sắp cạn."
            }
        },
        "scan": {
            "definition_vi": "(v) quét (mã vạch, tài liệu); đọc lướt nhanh; (n) sự quét",
            "examples_vi": [
                "Đĩa quang của máy tính đã quét thông tin về giá cả và đặt hàng vào hệ thống.",
                "Hãy nhìn lướt qua các lối đi xem bạn có tìm thấy thùng hàng bị thất lạc không."
            ],
            "collocations": [
                "scan a barcode",
                "scan a document",
                "scan the list",
                "optical scanner"
            ],
            "usage": {
                "structures": [
                    "scan + a barcode/label/document (quét mã vạch/nhãn/tài liệu)",
                    "scan + a page/list (đọc lướt nhanh qua trang giấy/danh sách)"
                ],
                "prepositions": ["into", "for"],
                "collocations": [
                    "handheld barcode scanner",
                    "scan items at checkout",
                    "scanned copy",
                    "quick scan"
                ],
                "tip": "Danh từ có đuôi -er là 'scanner' (máy quét mã vạch/tài liệu - thiết bị vật lý), không phải người."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "scanning",
                    "example": "High-speed barcode scanning has reduced warehouse check-in times.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Each warehouse clerk is equipped with a handheld wireless _____ to record stock levels.",
                "answer": "scanner",
                "base_word": "scan",
                "pos_hint": "danh từ chỉ thiết bị máy quét",
                "vi": "Mỗi nhân viên kho được trang bị một máy quét không dây cầm tay để ghi lại mức tồn kho."
            }
        },
        "subtract": {
            "definition_vi": "trừ đi, khấu trừ",
            "examples_vi": [
                "Ngay khi bạn tính tiền một món hàng trên máy, máy tính sẽ tự động trừ món hàng đó khỏi nhật ký tồn kho.",
                "Bất cứ ai làm việc kiểm kê đã quên trừ đi những mặt hàng bị hư hỏng khi mới giao đến và chưa bao giờ được đưa vào kho."
            ],
            "collocations": [
                "subtract from the total",
                "subtract damaged items",
                "addition and subtraction",
                "automatically subtract"
            ],
            "usage": {
                "structures": [
                    "subtract + A + from + B (trừ A khỏi B)"
                ],
                "prepositions": ["from"],
                "collocations": [
                    "subtract expenses from revenue",
                    "subtract the discount",
                    "subtract returned goods",
                    "basic subtraction"
                ],
                "tip": "Luôn đi kèm giới từ 'from' (subtract A FROM B = trừ A ra khỏi tổng B), đồng nghĩa với 'deduct A from B'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "subtractive",
                    "example": "The accounting module uses a subtractive method to calculate net stock.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "When calculating net profit, remember to _____ all operating expenses from gross revenue.",
                "answer": "subtract",
                "base_word": "subtract",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Khi tính lợi nhuận ròng, hãy nhớ trừ đi tất cả chi phí vận hành khỏi tổng doanh thu."
            }
        },
        "tedious": {
            "definition_vi": "tẻ nhạt, nhàm chán, đơn điệu và mất thời gian",
            "examples_vi": [
                "Đây có thể là công việc tẻ nhạt nhưng bạn sẽ thấy mừng vì số liệu tồn kho chính xác khi bước vào mùa bán hàng lễ hội bận rộn.",
                "Đếm hàng hóa suốt cả dịp cuối tuần là công việc tẻ nhạt nhất mà tôi có thể tưởng tượng ra."
            ],
            "collocations": [
                "tedious task",
                "tedious process",
                "tedious work",
                "long and tedious"
            ],
            "usage": {
                "structures": [
                    "a tedious + task/job/process/chore (một công việc/quy trình tẻ nhạt và tốn thời gian)"
                ],
                "prepositions": ["for"],
                "collocations": [
                    "tedious manual data entry",
                    "tedious paperwork",
                    "relieve tediousness",
                    "find the work tedious"
                ],
                "tip": "Thường đi kèm với 'time-consuming' hoặc 'repetitive' để mô tả các công việc thủ công nhàm chán như nhập liệu, kiểm đếm kho."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "tedium",
                    "example": "Barcode scanners have eliminated much of the tedium of annual stocktaking.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "tediousness",
                    "example": "Despite the tediousness of the audit, the clerks checked every single box.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "tedious",
                    "example": "Entering thousands of serial numbers by hand is a tedious task.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "tediously",
                    "example": "Before the software upgrade, invoices had to be tediously cross-checked by hand.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new optical recognition software automates the _____ process of entering receipt data manually.",
                "answer": "tedious",
                "base_word": "tedious",
                "pos_hint": "tính từ",
                "vi": "Phần mềm nhận dạng quang học mới giúp tự động hóa quy trình nhập dữ liệu biên lai thủ công vốn rất tẻ nhạt."
            }
        },
        "verify": {
            "definition_vi": "xác minh, kiểm chứng, đối chiếu cho chuẩn xác",
            "examples_vi": [
                "Tôi không thể xác minh độ chính xác của những con số này vì tôi đã không có mặt vào dịp cuối tuần kiểm kê kho.",
                "Quy trình kiểm kê giúp xác minh rằng bạn đã kiểm đếm đầy đủ tất cả các mặt hàng lẽ ra phải có trong cửa hàng."
            ],
            "collocations": [
                "verify the accuracy",
                "verify information",
                "verify shipments",
                "identity verification"
            ],
            "usage": {
                "structures": [
                    "verify + N (accuracy/figures/identity/receipt) (xác minh độ chính xác/số liệu/danh tính)",
                    "verify that + S + V (xác minh rằng...)"
                ],
                "prepositions": ["with", "by"],
                "collocations": [
                    "verify the contents of a package",
                    "independently verified",
                    "verification code",
                    "easily verifiable"
                ],
                "tip": "Từ vựng cực kỳ quan trọng trong TOEIC; chú ý danh từ 'verification' (sự xác minh: require verification) và tính từ 'verifiable' (có thể kiểm chứng được)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "verify",
                    "example": "Please verify the quantity of items received before signing the delivery slip.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "verification",
                    "example": "For security verification, please enter the six-digit code sent to your phone.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "verifiable",
                    "example": "All expense claims must be supported by verifiable receipts.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "verified",
                    "example": "Only verified vendors are permitted to bid on municipal supply contracts.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Upon _____ of your employment history, the human resources office will issue a formal contract.",
                "answer": "verification",
                "base_word": "verify",
                "pos_hint": "danh từ",
                "vi": "Sau khi xác minh lịch sử làm việc của bạn, phòng nhân sự sẽ phát hành hợp đồng chính thức."
            }
        }
    }
}


if __name__ == "__main__":
    import json

    scratch_path = r"C:\Users\LEGION\.gemini\antigravity\brain\dd06d532-873e-4cf4-997f-622fdb86edbc\scratch\batch_2.json"
    with open(scratch_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    expected_lessons = list(range(11, 21))
    assert sorted(BATCH_DATA.keys()) == expected_lessons, f"Expected lessons {expected_lessons}, got {sorted(BATCH_DATA.keys())}"

    total_words = 0
    required_keys = {"definition_vi", "examples_vi", "collocations", "usage", "extra_families", "srs_sentence"}
    for lid in expected_lessons:
        lesson_words = [w["word"] for w in raw[str(lid)]["words"]]
        batch_words = list(BATCH_DATA[lid].keys())
        assert sorted(lesson_words) == sorted(batch_words), f"Lesson {lid} word mismatch: {set(lesson_words) ^ set(batch_words)}"
        for w, entry in BATCH_DATA[lid].items():
            missing = required_keys - set(entry.keys())
            assert not missing, f"Lesson {lid} word '{w}' missing keys: {missing}"
            assert entry["definition_vi"].strip(), f"Empty definition_vi for '{w}'"
            assert len(entry["examples_vi"]) >= 1 and all(x.strip() for x in entry["examples_vi"]), f"Bad examples_vi for '{w}'"
            assert len(entry["collocations"]) == 4, f"Expected 4 collocations for '{w}'"
            assert len(entry["usage"]["collocations"]) == 4, f"Expected 4 usage.collocations for '{w}'"
            assert entry["usage"]["tip"].strip(), f"Empty usage.tip for '{w}'"
            assert len(entry["extra_families"]) >= 1, f"Empty extra_families for '{w}'"
            for fam in entry["extra_families"]:
                assert fam["pos"] in {"verb", "noun", "adjective", "adverb"}, f"Invalid pos in extra_families for '{w}': {fam}"
                assert fam["pos_source"] == "extended", f"Invalid pos_source for '{w}'"
            srs = entry["srs_sentence"]
            assert "_____" in srs["en"], f"Missing blank in srs_sentence for '{w}'"
            assert srs["answer"].strip() and srs["base_word"] == w and srs["pos_hint"].strip() and srs["vi"].strip(), f"Bad srs_sentence for '{w}'"
            total_words += 1

    assert total_words == 119, f"Expected 119 words, got {total_words}"
    print(f"SUCCESS: Verified {len(expected_lessons)} lessons (11..20) and {total_words} words in vocab_data_batch2.py!")
