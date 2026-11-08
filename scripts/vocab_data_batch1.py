# -*- coding: utf-8 -*-
"""
Vocabulary data enrichment for Lessons 1 to 10 (120 words).
"""

BATCH_DATA = {
    1: {
        "abide by": {
            "definition_vi": "tuân thủ, chấp hành (quy định, quyết định, hợp đồng)",
            "examples_vi": [
                "Hai bên đã đồng ý tuân thủ phán quyết của thẩm phán.",
                "Trong nhiều năm qua, ông ấy luôn giữ vững cam kết tăng lương hàng năm cho nhân viên."
            ],
            "collocations": [
                "abide by the rules",
                "abide by the decision",
                "abide by the terms of the contract",
                "strictly abide by"
            ],
            "usage": {
                "structures": [
                    "abide by + N (rules / law / agreement / decision)",
                    "agree / promise / refuse to abide by + N"
                ],
                "prepositions": ["by"],
                "collocations": [
                    "abide by the terms",
                    "abide by the regulations",
                    "abide by the court's ruling",
                    "abide by a commitment"
                ],
                "tip": "Trong TOEIC Part 5, khi thấy chỗ trống đứng trước giới từ 'by' và tân ngữ chỉ luật lệ/hợp đồng, hãy chọn ngay động từ 'abide'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "abide",
                    "example": "All contractors must abide by the safety regulations on site.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "abidance",
                    "example": "Strict abidance by the terms of the lease is required of all tenants.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "abiding",
                    "example": "Our founder had an abiding commitment to business ethics and quality.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "abidingly",
                    "example": "The staff remained abidingly loyal to the company during the merger.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "For the past decade, our corporation has strictly _____ by all environmental regulations.",
                "answer": "abided",
                "base_word": "abide by",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed)",
                "vi": "Trong suốt thập kỷ qua, tập đoàn của chúng tôi đã tuân thủ nghiêm ngặt mọi quy định về môi trường."
            }
        },
        "agreement": {
            "definition_vi": "hợp đồng, thỏa thuận; sự đồng tình, nhất trí",
            "examples_vi": [
                "Chủ nhà và người thuê nhà đã thống nhất rằng tiền thuê nhà nên được tính theo tỷ lệ đến giữa tháng.",
                "Theo hợp đồng, bên cung cấp dịch vụ ăn uống cũng sẽ cung cấp hoa cho sự kiện."
            ],
            "collocations": [
                "reach an agreement",
                "sign an agreement",
                "be in agreement",
                "according to the agreement"
            ],
            "usage": {
                "structures": [
                    "reach / come to / sign / enter into an agreement",
                    "be in agreement (with sb) (on/about sth)"
                ],
                "prepositions": ["in", "on", "with", "between"],
                "collocations": [
                    "mutual agreement",
                    "verbal agreement",
                    "contractual agreement",
                    "violate an agreement"
                ],
                "tip": "Chú ý cụm cố định 'be in agreement' (= agree) và 'reach an agreement' (đạt được thỏa thuận) rất hay xuất hiện trong đề thi."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "agreeably",
                    "example": "We were agreeably surprised by the rapid growth in third-quarter revenue.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "If both parties are _____ to the proposed terms, we can sign the contract tomorrow morning.",
                "answer": "agreeable",
                "base_word": "agreement",
                "pos_hint": "tính từ",
                "vi": "Nếu cả hai bên đều đồng ý với các điều khoản được đề xuất, chúng ta có thể ký hợp đồng vào sáng mai."
            }
        },
        "assurance": {
            "definition_vi": "sự cam đoan, lời bảo đảm; sự tự tin",
            "examples_vi": [
                "Nhân viên bán hàng đã cam đoan rằng chiếc bàn phím bị thiếu sẽ được thay thế vào ngày hôm sau.",
                "Sự tự tin của cô ấy khiến mọi người dễ dàng hiểu tại sao cô lại phụ trách cuộc đàm phán."
            ],
            "collocations": [
                "give an assurance",
                "quality assurance",
                "self-assurance",
                "seek assurances from"
            ],
            "usage": {
                "structures": [
                    "give / offer (sb) an assurance (that + mệnh đề)",
                    "assurance of + N"
                ],
                "prepositions": ["of", "from", "that"],
                "collocations": [
                    "quality assurance department",
                    "written assurance",
                    "firm assurance",
                    "solemn assurance"
                ],
                "tip": "Cụm danh từ ghép 'quality assurance' (đảm bảo chất lượng) và cấu trúc 'give an assurance that...' xuất hiện rất thường xuyên trong Part 5 & 7."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "assured",
                    "example": "You can rest assured that your order will be delivered before Friday.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The project manager _____ the board of directors that the construction would be completed on schedule.",
                "answer": "assured",
                "base_word": "assurance",
                "pos_hint": "động từ chia quá khứ đơn (V-ed)",
                "vi": "Giám đốc dự án đã cam đoan với hội đồng quản trị rằng việc xây dựng sẽ hoàn thành đúng tiến độ."
            }
        },
        "cancellation": {
            "definition_vi": "sự hủy bỏ, sự bãi bỏ (chuyến bay, hợp đồng, đặt chỗ)",
            "examples_vi": [
                "Việc hủy chuyến bay đã gây ra nhiều rắc rối cho cô ấy trong suốt phần còn lại của tuần.",
                "Điều khoản hủy bỏ xuất hiện ở mặt sau của hợp đồng."
            ],
            "collocations": [
                "cancellation clause",
                "cancellation fee",
                "flight cancellation",
                "last-minute cancellation"
            ],
            "usage": {
                "structures": [
                    "cancellation of + N",
                    "cancellation + N (clause / fee / policy / notice)"
                ],
                "prepositions": ["of", "for"],
                "collocations": [
                    "cancellation policy",
                    "subject to cancellation",
                    "notice of cancellation",
                    "order cancellation"
                ],
                "tip": "Danh từ 'cancellation' thường đứng trước một danh từ khác để tạo cụm danh từ ghép như 'cancellation fee/clause/policy'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "cancelable",
                    "example": "Please note that promotional airline tickets are non-refundable and non-cancelable.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Customers who _____ their reservation less than 24 hours in advance will be charged a small fee.",
                "answer": "cancel",
                "base_word": "cancellation",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Khách hàng hủy đặt chỗ trước ít hơn 24 giờ sẽ bị tính một khoản phí nhỏ."
            }
        },
        "determine": {
            "definition_vi": "xác định, tìm ra; quyết định, định đoạt",
            "examples_vi": [
                "Sau khi đọc hợp đồng, tôi vẫn không thể xác định được liệu công ty chúng ta có phải chịu trách nhiệm trả lương truy lĩnh hay không.",
                "Kỹ năng của những người đàm phán công đoàn sẽ quyết định liệu nhà máy ô tô có mở cửa vào tuần tới hay không."
            ],
            "collocations": [
                "determine the cause",
                "determine whether",
                "be determined to V",
                "determine the price"
            ],
            "usage": {
                "structures": [
                    "determine + whether / if / wh-clause",
                    "be determined to + V (quyết tâm làm gì)"
                ],
                "prepositions": ["by", "to"],
                "collocations": [
                    "determine eligibility",
                    "determine the outcome",
                    "determine the feasibility",
                    "yet to be determined"
                ],
                "tip": "Thường đi theo sau bởi mệnh đề bắt đầu bằng 'whether/if' hoặc từ để hỏi (how, what, why) để diễn tả việc xác định một thông tin."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "determine",
                    "example": "An independent auditor will determine the exact value of the company's assets.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "determination",
                    "example": "Her fierce determination helped the startup survive its first two years.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "determined",
                    "example": "Our sales team is determined to exceed this quarter's revenue targets.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "determinedly",
                    "example": "The committee worked determinedly to resolve the budget deficit before Friday.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The final price of the software package will be _____ by the number of user licenses required.",
                "answer": "determined",
                "base_word": "determine",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed - bị động)",
                "vi": "Giá cuối cùng của gói phần mềm sẽ được quyết định bởi số lượng giấy phép người dùng được yêu cầu."
            }
        },
        "engage": {
            "definition_vi": "tham gia vào, dấn thân vào; thu hút, lôi cuốn; thuê (nhân sự/dịch vụ)",
            "examples_vi": [
                "Trước khi tham gia vào một lĩnh vực kinh doanh mới, điều quan trọng là phải nghiên cứu kỹ lưỡng.",
                "Anh ấy đã lôi cuốn chúng tôi vào một cuộc thảo luận hấp dẫn về luật kinh doanh hiện hành."
            ],
            "collocations": [
                "engage in business",
                "engage in a discussion",
                "engage a consultant",
                "be engaged in"
            ],
            "usage": {
                "structures": [
                    "engage in + N / V-ing (tham gia vào)",
                    "engage + sb + in + N (lôi cuốn ai vào việc gì)",
                    "be engaged to + sb (đính hôn với ai)"
                ],
                "prepositions": ["in", "with", "to"],
                "collocations": [
                    "engage in negotiations",
                    "engage legal counsel",
                    "actively engage with customers",
                    "prior engagement"
                ],
                "tip": "Giới từ kinh điển đi kèm với 'engage' (mang nghĩa tham gia) là 'in': 'engage in + N/V-ing' (= participate in)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "engage",
                    "example": "The firm decided to engage an outside agency to handle public relations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "engagement",
                    "example": "The director had to decline the invitation due to a prior business engagement.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "engaging",
                    "example": "The keynote speaker gave a very engaging presentation on market trends.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "engagingly",
                    "example": "She spoke so engagingly that the audience stayed for an extra hour of questions.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The CEO apologized for missing the awards banquet due to a prior business _____ in Tokyo.",
                "answer": "engagement",
                "base_word": "engage",
                "pos_hint": "danh từ số ít",
                "vi": "Vị giám đốc điều hành đã xin lỗi vì vắng mặt tại bữa tiệc trao giải do có một lịch hẹn công việc từ trước ở Tokyo."
            }
        },
        "establish": {
            "definition_vi": "thành lập, thiết lập; khẳng định (vị thế, uy tín)",
            "examples_vi": [
                "Thông qua nhiều cuốn sách và các cuộc phỏng vấn của mình, Tiến sĩ Wan đã khẳng định mình là một chuyên gia có uy tín về giải quyết xung đột.",
                "Việc sáp nhập hai công ty đã tạo lập nên một tập đoàn mới hùng mạnh."
            ],
            "collocations": [
                "establish a company",
                "establish a reputation",
                "establish guidelines",
                "establish oneself as"
            ],
            "usage": {
                "structures": [
                    "establish + N (company / relationship / policy)",
                    "establish oneself as + N (khẳng định bản thân là...)"
                ],
                "prepositions": ["as", "in"],
                "collocations": [
                    "well-established firm",
                    "establish a committee",
                    "establish diplomatic relations",
                    "newly established branch"
                ],
                "tip": "Tính từ phân từ 'established' hoặc 'well-established' (lâu đời, có uy tín vững chắc) thường đứng trước danh từ chỉ công ty/tổ chức."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "establish",
                    "example": "The bank plans to establish three new branches in the metropolitan area.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "establishment",
                    "example": "The establishment of a regional headquarters will improve distribution speed.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "established",
                    "example": "It is difficult for newcomers to compete with well-established brands.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The _____ of the new safety committee has significantly reduced workplace accidents.",
                "answer": "establishment",
                "base_word": "establish",
                "pos_hint": "danh từ",
                "vi": "Việc thành lập ủy ban an toàn mới đã làm giảm đáng kể các vụ tai nạn lao động."
            }
        },
        "obligate": {
            "definition_vi": "bắt buộc, ép buộc (về mặt pháp lý hoặc đạo đức)",
            "examples_vi": [
                "Nhà thầu bị ràng buộc bởi hợp đồng phải làm việc 40 giờ một tuần.",
                "Tôi cảm thấy có nghĩa vụ phải hoàn thành dự án mặc dù tôi có thể sử dụng quyền lựa chọn nghỉ việc của mình."
            ],
            "collocations": [
                "be obligated to V",
                "feel obligated to",
                "legal obligation",
                "contractually obligated"
            ],
            "usage": {
                "structures": [
                    "obligate + sb + to V",
                    "be / feel obligated to + V"
                ],
                "prepositions": ["to", "by"],
                "collocations": [
                    "fulfill an obligation",
                    "meet one's obligations",
                    "without obligation",
                    "obligatory attendance"
                ],
                "tip": "Hầu như luôn dùng ở dạng bị động 'be/feel obligated to V' (có nghĩa vụ/bị bắt buộc phải làm gì)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "obligatorily",
                    "example": "All visitors to the chemical plant are obligatorily required to wear protective eyewear.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Under the terms of the lease, tenants are under no _____ to renew their contract after one year.",
                "answer": "obligation",
                "base_word": "obligate",
                "pos_hint": "danh từ",
                "vi": "Theo các điều khoản của hợp đồng thuê, người thuê nhà không có nghĩa vụ phải gia hạn hợp đồng sau một năm."
            }
        },
        "party": {
            "definition_vi": "bên (tham gia hợp đồng, tranh chấp pháp lý); bữa tiệc, đoàn/nhóm người",
            "examples_vi": [
                "Các bên đã đồng ý dàn xếp vụ tranh chấp hợp đồng của họ.",
                "Bên soạn thảo hợp đồng có một lợi thế rõ rệt."
            ],
            "collocations": [
                "both parties",
                "third party",
                "interested party",
                "contracting parties"
            ],
            "usage": {
                "structures": [
                    "the party / parties to + N (the contract / agreement)",
                    "third-party + N (vendor / supplier / insurance)"
                ],
                "prepositions": ["to", "in"],
                "collocations": [
                    "all parties concerned",
                    "be a party to an agreement",
                    "third-party software",
                    "involved parties"
                ],
                "tip": "Trong ngữ cảnh pháp lý và hợp đồng TOEIC, 'party' không dịch là 'bữa tiệc' mà luôn mang nghĩa là 'bên đối tác/bên tham gia'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "party",
                    "example": "Both parties signed the non-disclosure agreement before starting negotiations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "partisan",
                    "example": "The mediator remained strictly non-partisan throughout the labor dispute.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All _____ involved in the merger must sign the confidentiality agreement before Friday.",
                "answer": "parties",
                "base_word": "party",
                "pos_hint": "danh từ số nhiều",
                "vi": "Tất cả các bên liên quan đến vụ sáp nhập phải ký thỏa thuận bảo mật trước thứ Sáu."
            }
        },
        "provision": {
            "definition_vi": "điều khoản (trong hợp đồng, văn bản luật); sự cung cấp, sự dự phòng",
            "examples_vi": [
                "Người cha đã lập các khoản dự phòng cho con cái thông qua di chúc của mình.",
                "Hợp đồng có một điều khoản giải quyết cách thức thanh toán nếu John bị mất việc."
            ],
            "collocations": [
                "make provisions for",
                "contractual provision",
                "under the provisions of",
                "provision of services"
            ],
            "usage": {
                "structures": [
                    "make provision(s) for + N (chuẩn bị/dự phòng cho)",
                    "contain / include a provision (that + mệnh đề)"
                ],
                "prepositions": ["for", "of", "under"],
                "collocations": [
                    "key provision",
                    "special provision",
                    "legal provisions",
                    "penalty provision"
                ],
                "tip": "Khi đi với hợp đồng (contract/law), 'provision' đồng nghĩa với 'clause' hoặc 'stipulation' (điều khoản)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "provisional",
                    "example": "The committee issued a provisional approval pending the final safety inspection.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "provisionally",
                    "example": "The annual conference has been provisionally scheduled for the third week of October.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The telecommunications _____ announced that it would upgrade its fiber-optic network next month.",
                "answer": "provider",
                "base_word": "provision",
                "pos_hint": "danh từ chỉ người/tổ chức",
                "vi": "Nhà cung cấp dịch vụ viễn thông đã thông báo rằng họ sẽ nâng cấp mạng cáp quang vào tháng tới."
            }
        },
        "resolve": {
            "definition_vi": "giải quyết, tháo gỡ (vấn đề, tranh chấp); quyết tâm (làm gì); sự kiên quyết",
            "examples_vi": [
                "Người hòa giải đã có thể giải quyết vấn đề làm hài lòng tất cả mọi người.",
                "Doanh nhân đó đã quyết tâm dọn sạch tất cả các hồ sơ trước cuối tuần."
            ],
            "collocations": [
                "resolve a dispute",
                "resolve an issue",
                "resolve a conflict",
                "resolve to do"
            ],
            "usage": {
                "structures": [
                    "resolve + N (problem / issue / dispute / crisis)",
                    "resolve + to V (quyết tâm làm gì)"
                ],
                "prepositions": ["to", "by"],
                "collocations": [
                    "conflict resolution",
                    "pass a resolution",
                    "peacefully resolve",
                    "quickly resolve"
                ],
                "tip": "Thường đi kèm các tân ngữ chỉ rắc rối như 'problem, issue, dispute, complaint, conflict'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "resolve",
                    "example": "Our technical support team is working hard to resolve the network outage.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "resolution",
                    "example": "The board passed a resolution to expand operations into Southeast Asia.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "resolute",
                    "example": "The chief executive remained resolute in her decision to restructure the division.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "resolutely",
                    "example": "The union leaders resolutely opposed any reduction in health benefits.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The board of directors passed a formal _____ to allocate more funds to research and development.",
                "answer": "resolution",
                "base_word": "resolve",
                "pos_hint": "danh từ số ít",
                "vi": "Hội đồng quản trị đã thông qua một nghị quyết chính thức nhằm phân bổ thêm ngân sách cho nghiên cứu và phát triển."
            }
        },
        "specific": {
            "definition_vi": "cụ thể, rõ ràng, chi tiết, đặc trưng",
            "examples_vi": [
                "Khiếu nại cụ thể của khách hàng đã không được giải quyết trong email của anh ta.",
                "Trong một bản hợp đồng, một từ cụ thể có thể làm thay đổi ý nghĩa một cách đáng kể."
            ],
            "collocations": [
                "be specific about",
                "specific requirements",
                "specific instructions",
                "specific details"
            ],
            "usage": {
                "structures": [
                    "specific to + N (đặc thù/riêng biệt cho cái gì)",
                    "meet the specifications (đạt các thông số kỹ thuật)"
                ],
                "prepositions": ["to", "about"],
                "collocations": [
                    "technical specifications",
                    "for a specific purpose",
                    "industry-specific knowledge",
                    "specify the date"
                ],
                "tip": "Danh từ 'specifications' (thường ở dạng số nhiều) mang nghĩa 'thông số kỹ thuật/yêu cầu chi tiết', rất hay đi với động từ 'meet'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "specifically",
                    "example": "This software was specifically designed for small accounting firms.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new machinery was built strictly according to the client's technical _____.",
                "answer": "specifications",
                "base_word": "specific",
                "pos_hint": "danh từ số nhiều",
                "vi": "Hệ thống máy móc mới được chế tạo hoàn toàn tuân theo các thông số kỹ thuật của khách hàng."
            }
        }
    },
    2: {
        "attract": {
            "definition_vi": "thu hút, hấp dẫn, lôi cuốn (khách hàng, sự chú ý, đầu tư)",
            "examples_vi": [
                "Gian trưng bày đã thu hút rất nhiều người tại hội nghị.",
                "Quảng cáo mới lại thu hút nhầm đối tượng khách hàng vào cửa hàng."
            ],
            "collocations": [
                "attract customers",
                "attract attention",
                "attract investment",
                "tourist attraction"
            ],
            "usage": {
                "structures": [
                    "attract + sb/sth (to + N)",
                    "attract attention / interest / criticism"
                ],
                "prepositions": ["to", "by"],
                "collocations": [
                    "attract new clients",
                    "attractive price",
                    "main attraction",
                    "attract qualified applicants"
                ],
                "tip": "Tính từ 'attractive' ngoài nghĩa 'đẹp' còn rất hay đi với 'price/offer/salary/package' (mức giá/đãi ngộ hấp dẫn)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "attractively",
                    "example": "Merchandise that is attractively displayed tends to sell much faster.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The company offers a highly _____ benefits package in order to recruit top engineering talent.",
                "answer": "attractive",
                "base_word": "attract",
                "pos_hint": "tính từ",
                "vi": "Công ty đưa ra một gói phúc lợi vô cùng hấp dẫn nhằm tuyển dụng những nhân tài kỹ thuật hàng đầu."
            }
        },
        "compare": {
            "definition_vi": "so sánh, đối chiếu; sánh được với",
            "examples_vi": [
                "Một khi khách hàng đã so sánh hai sản phẩm, sự lựa chọn của cô ấy trở nên thật dễ dàng.",
                "Giá của thương hiệu này khá cao khi so với các thương hiệu khác trên thị trường."
            ],
            "collocations": [
                "compare prices",
                "compared to / with",
                "in comparison with",
                "beyond compare"
            ],
            "usage": {
                "structures": [
                    "compare A with/to B",
                    "compared to/with + N (khi so với - thường đứng đầu hoặc cuối câu)"
                ],
                "prepositions": ["to", "with"],
                "collocations": [
                    "draw a comparison",
                    "pale in comparison",
                    "comparable quality",
                    "favorable comparison"
                ],
                "tip": "Đứng đầu câu trước dấu phẩy và đi với giới từ 'to/with' luôn là phân từ quá khứ 'Compared to/with...' (So với...)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "comparably",
                    "example": "Our new laptop performs comparably to models that cost twice as much.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "In _____ with last year's figures, domestic sales have risen by nearly fifteen percent.",
                "answer": "comparison",
                "base_word": "compare",
                "pos_hint": "danh từ",
                "vi": "So với số liệu năm ngoái, doanh số bán hàng trong nước đã tăng gần mười lăm phần trăm."
            }
        },
        "competition": {
            "definition_vi": "sự cạnh tranh; cuộc thi đấu; đối thủ cạnh tranh",
            "examples_vi": [
                "Trong cuộc cạnh tranh giành thực khách buổi chiều, nhà hàng của Hector đã vươn lên dẫn đầu.",
                "Công ty đã quyết định không tham gia vào cuộc cạnh tranh ngày càng gay gắt để giành vị thế thống lĩnh trên thị trường bán dẫn."
            ],
            "collocations": [
                "fierce competition",
                "compete with / against",
                "competitive edge",
                "competitive prices"
            ],
            "usage": {
                "structures": [
                    "competition between A and B (for sth)",
                    "compete with/against sb for sth"
                ],
                "prepositions": ["for", "with", "against", "between"],
                "collocations": [
                    "intense competition",
                    "stay ahead of the competition",
                    "competitive advantage",
                    "outdo the competition"
                ],
                "tip": "Chú ý phân biệt hai danh từ: 'competition' (sự cạnh tranh / cuộc thi) và 'competitor' (đối thủ cạnh tranh - danh từ đếm được)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "competitor",
                    "example": "Our main competitor just launched a similar product at a lower price.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "competitively",
                    "example": "All of our organic food products are competitively priced.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Because our products are _____ priced, we have been able to capture a large share of the market.",
                "answer": "competitively",
                "base_word": "competition",
                "pos_hint": "trạng từ",
                "vi": "Bởi vì sản phẩm của chúng tôi được định giá một cách cạnh tranh, chúng tôi đã có thể chiếm lĩnh một thị phần lớn."
            }
        },
        "consume": {
            "definition_vi": "tiêu thụ, sử dụng hết (năng lượng, thời gian, tài nguyên); choáng hết (tâm trí)",
            "examples_vi": [
                "Các kế hoạch kinh doanh đã chiếm hết mọi sự chú ý của Fritz vào mùa thu này.",
                "Chiếc máy in này tiêu tốn nhiều mực hơn chiếc máy in ở tầng dưới."
            ],
            "collocations": [
                "consume energy",
                "time-consuming",
                "consumer goods",
                "fuel consumption"
            ],
            "usage": {
                "structures": [
                    "consume + N (energy / time / resources / food)",
                    "be consumed with/by + N (bị choáng ngợp bởi)"
                ],
                "prepositions": ["by", "with"],
                "collocations": [
                    "consumer spending",
                    "consumer electronics",
                    "energy consumption",
                    "consumable supplies"
                ],
                "tip": "Danh từ chỉ người 'consumer' (người tiêu dùng) và danh từ chỉ sự việc 'consumption' (sự tiêu thụ) xuất hiện cực nhiều trong bài đọc TOEIC."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "consumption",
                    "example": "Installing LED lighting has drastically reduced our electricity consumption.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "consuming",
                    "example": "Auditing the international accounts was a very time-consuming process.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The government closely monitors _____ spending to evaluate the health of the national economy.",
                "answer": "consumer",
                "base_word": "consume",
                "pos_hint": "danh từ (đứng trước danh từ khác làm định ngữ)",
                "vi": "Chính phủ theo dõi chặt chẽ chi tiêu của người tiêu dùng để đánh giá sức khỏe của nền kinh tế quốc gia."
            }
        },
        "convince": {
            "definition_vi": "thuyết phục (ai đó tin vào điều gì hoặc làm gì)",
            "examples_vi": [
                "Người bán hàng đã thuyết phục khách hàng mua toàn bộ số bút tồn kho của anh ta.",
                "Trước khi một doanh nghiệp có thể thuyết phục khách hàng rằng họ cung cấp sản phẩm chất lượng, họ phải thuyết phục được đội ngũ tiếp thị của chính mình."
            ],
            "collocations": [
                "convince sb to do sth",
                "convince sb of sth",
                "be convinced that",
                "convincing argument"
            ],
            "usage": {
                "structures": [
                    "convince + sb + to V",
                    "convince + sb + of + N / that + mệnh đề",
                    "be convinced of + N / that + mệnh đề (tin chắc rằng)"
                ],
                "prepositions": ["of", "to", "that"],
                "collocations": [
                    "convincing evidence",
                    "hard to convince",
                    "fully convinced",
                    "convince investors"
                ],
                "tip": "'Convince' là ngoại động từ, sau nó bắt buộc phải có tân ngữ chỉ người (convince sb to V / convince sb that...), trừ khi chia bị động (be convinced that...)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "convince",
                    "example": "We need solid data to convince the board to approve the expansion.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "conviction",
                    "example": "She spoke with deep conviction about the importance of customer service.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "convincing",
                    "example": "The sales director presented a very convincing case for hiring more staff.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "convincingly",
                    "example": "The applicant demonstrated convincingly that he had the skills for the job.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The marketing team made a very _____ presentation that won over the skeptical investors.",
                "answer": "convincing",
                "base_word": "convince",
                "pos_hint": "tính từ (đuôi -ing bổ nghĩa cho sự vật)",
                "vi": "Đội ngũ tiếp thị đã thực hiện một bài thuyết trình rất thuyết phục khiến các nhà đầu tư hoài nghi cũng phải đồng tình."
            }
        },
        "currently": {
            "definition_vi": "hiện tại, hiện nay, vào lúc này",
            "examples_vi": [
                "Hiện tại chúng tôi đang tìm hiểu các kế hoạch để nâng cấp mẫu sản phẩm MX3.",
                "Hiện nay, khách hàng đang đòi hỏi mức chiết khấu lớn cho các đơn hàng số lượng nhiều."
            ],
            "collocations": [
                "currently available",
                "currently under construction",
                "currently employed",
                "currently working on"
            ],
            "usage": {
                "structures": [
                    "be + currently + V-ing / V3-ed / Adj",
                    "Currently, + S + V (thường chia thì hiện tại tiếp diễn hoặc hiện tại đơn)"
                ],
                "prepositions": ["at", "in"],
                "collocations": [
                    "currently in progress",
                    "currently under review",
                    "currently unavailable",
                    "currently hold the position"
                ],
                "tip": "Khi thấy trạng từ 'currently' trong câu, động từ chính thường chia ở thì hiện tại tiếp diễn (is/are + V-ing) hoặc hiện tại đơn."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "currency",
                    "example": "Foreign currency exchange services are available at the main branch.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "current",
                    "example": "Please make sure we have your current mailing address on file.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "currently",
                    "example": "The system is currently undergoing scheduled maintenance.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All job applicants must submit a resume along with two references from _____ or former employers.",
                "answer": "current",
                "base_word": "currently",
                "pos_hint": "tính từ",
                "vi": "Tất cả các ứng viên xin việc phải nộp sơ yếu lý lịch cùng với hai thư giới thiệu từ người sử dụng lao động hiện tại hoặc trước đây."
            }
        },
        "fad": {
            "definition_vi": "mốt nhất thời, trào lưu tạm bợ, cơn sốt ngắn hạn",
            "examples_vi": [
                "Váy ngắn từng là một mốt nhất thời được cho là đã lỗi thời, nhưng giờ đây nó đang quay trở lại.",
                "Gu thẩm mỹ cổ điển có vẻ nhàm chán nhưng đã được chứng minh là đứng vững trước các trào lưu nhất thời."
            ],
            "collocations": [
                "passing fad",
                "latest fad",
                "mere fad",
                "resist fads"
            ],
            "usage": {
                "structures": [
                    "a passing fad (một trào lưu thoáng qua)",
                    "follow / resist a fad"
                ],
                "prepositions": ["for", "in"],
                "collocations": [
                    "diet fad",
                    "fashion fad",
                    "short-lived fad",
                    "temporary fad"
                ],
                "tip": "Trong bài đọc Part 7 về Marketing, 'fad' luôn mang hàm ý trào lưu ngắn hạn (short-lived), đối lập với xu hướng lâu dài (long-term trend)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "fad",
                    "example": "Many analysts dismissed the new gadget as just a passing fad.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "faddish",
                    "example": "Investors generally avoid companies that rely on faddish consumer products.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "faddishly",
                    "example": "The boutique caters to teenagers who dress faddishly.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Rather than investing in _____ products, our firm focuses on household essentials with steady demand.",
                "answer": "faddish",
                "base_word": "fad",
                "pos_hint": "tính từ",
                "vi": "Thay vì đầu tư vào các sản phẩm chạy theo mốt nhất thời, công ty chúng tôi tập trung vào các nhu yếu phẩm gia đình có nhu cầu ổn định."
            }
        },
        "inspiration": {
            "definition_vi": "nguồn cảm hứng, sự truyền cảm hứng; ý tưởng sáng tạo chợt đến",
            "examples_vi": [
                "Công việc của anh ấy là một nguồn cảm hứng cho phòng tiếp thị.",
                "Doanh số bán hàng cao của Marta ở Tây Ban Nha là nguồn cảm hứng cho các đại diện bán hàng châu Âu khác."
            ],
            "collocations": [
                "draw inspiration from",
                "be an inspiration to",
                "source of inspiration",
                "sudden inspiration"
            ],
            "usage": {
                "structures": [
                    "an inspiration to + sb",
                    "draw / find / get inspiration from + N"
                ],
                "prepositions": ["to", "for", "from"],
                "collocations": [
                    "creative inspiration",
                    "constant inspiration",
                    "serve as an inspiration",
                    "lack inspiration"
                ],
                "tip": "Động từ tương ứng 'inspire' thường đi với cấu trúc 'inspire sb to V' (truyền cảm hứng cho ai làm gì)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "inspire",
                    "example": "Her dedication inspired the entire team to work harder.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "inspiration",
                    "example": "The architect drew inspiration from traditional Japanese gardens.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "inspirational",
                    "example": "The founder gave an inspirational speech at the annual company retreat.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "inspirationally",
                    "example": "She led the department inspirationally through a difficult transition.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The keynote speaker delivered an _____ talk about overcoming obstacles in entrepreneurship.",
                "answer": "inspirational",
                "base_word": "inspiration",
                "pos_hint": "tính từ",
                "vi": "Diễn giả chính đã có một bài phát biểu đầy cảm hứng về việc vượt qua những trở ngại trong quá trình khởi nghiệp."
            }
        },
        "market": {
            "definition_vi": "tiếp thị, tung ra thị trường (v.); thị trường, sức cầu đối với sản phẩm (n.)",
            "examples_vi": [
                "Khi Omar mới bắt đầu làm món tương ớt ngọt, anh đã tiếp thị chúng tận nơi cho các cửa hàng thực phẩm cao cấp.",
                "Thị trường quần áo màu sắc sặc sỡ rất sôi động vào năm ngoái, nhưng năm nay lại đang chuyển dịch khá chậm chạp."
            ],
            "collocations": [
                "target market",
                "market share",
                "on the market",
                "market research"
            ],
            "usage": {
                "structures": [
                    "market + N + to sb (tiếp thị sản phẩm tới đối tượng nào)",
                    "the market for + N (thị trường tiêu thụ cho sản phẩm gì)"
                ],
                "prepositions": ["for", "to", "on", "in"],
                "collocations": [
                    "put on the market",
                    "housing market",
                    "competitive market",
                    "emerging market"
                ],
                "tip": "Chú ý giới từ: 'on the market' (đang được bày bán trên thị trường) và 'the market for + N' (nhu cầu thị trường đối với mặt hàng gì)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "marketer",
                    "example": "Digital marketers use social media analytics to reach younger consumers.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Improving the packaging design will make our organic tea much more _____ to overseas buyers.",
                "answer": "marketable",
                "base_word": "market",
                "pos_hint": "tính từ",
                "vi": "Việc cải thiện thiết kế bao bì sẽ giúp trà hữu cơ của chúng ta dễ tiêu thụ hơn nhiều đối với người mua ở nước ngoài."
            }
        },
        "persuasion": {
            "definition_vi": "sự thuyết phục, tài thuyết phục; niềm tin vững chắc",
            "examples_vi": [
                "Hội thảo giảng dạy các kỹ thuật thuyết phục nhằm gia tăng doanh số bán hàng.",
                "Dưới sự thuyết phục của anh ấy, cô đã quay lại trường để học bằng Thạc sĩ Quản trị Kinh doanh (MBA)."
            ],
            "collocations": [
                "powers of persuasion",
                "art of persuasion",
                "gentle persuasion",
                "under sb's persuasion"
            ],
            "usage": {
                "structures": [
                    "persuade + sb + to V (thuyết phục ai làm gì)",
                    "persuade + sb + into V-ing / out of V-ing"
                ],
                "prepositions": ["of", "by", "under"],
                "collocations": [
                    "persuasive argument",
                    "persuasive speaker",
                    "skillful persuasion",
                    "take a lot of persuasion"
                ],
                "tip": "Gia đình từ 'persuade (v) - persuasion (n) - persuasive (adj) - persuasively (adv)' là nhóm từ vựng kinh điển trong TOEIC Part 5."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "persuade",
                    "example": "We finally persuaded the client to sign a two-year service contract.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "persuasion",
                    "example": "After a bit of gentle persuasion, Mr. Kim agreed to chair the committee.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "persuasive",
                    "example": "A successful salesperson must be both knowledgeable and persuasive.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "persuasively",
                    "example": "The attorney argued persuasively that the patent had not been infringed.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Thanks to her _____ negotiation skills, we secured a 15 percent discount from the supplier.",
                "answer": "persuasive",
                "base_word": "persuasion",
                "pos_hint": "tính từ",
                "vi": "Nhờ kỹ năng đàm phán đầy thuyết phục của cô ấy, chúng tôi đã giành được mức chiết khấu 15 phần trăm từ nhà cung cấp."
            }
        },
        "productive": {
            "definition_vi": "năng suất cao, có hiệu quả, sinh lời nhiều",
            "examples_vi": [
                "Cuộc họp bán hàng kém hiệu quả đã dẫn đến nhiều lời phàn nàn từ nhân viên.",
                "Alonzo rất hào hứng về đội ngũ nhân viên làm việc đầy năng suất của mình."
            ],
            "collocations": [
                "productive meeting",
                "highly productive",
                "productive workforce",
                "increase productivity"
            ],
            "usage": {
                "structures": [
                    "be productive (of + N)",
                    "boost / increase / improve productivity"
                ],
                "prepositions": ["of", "in"],
                "collocations": [
                    "productive discussion",
                    "workplace productivity",
                    "counterproductive",
                    "productive capacity"
                ],
                "tip": "Phân biệt kỹ hai tính từ của 'produce': 'productive' (có năng suất/hiệu quả cao) và 'produced' (được sản xuất)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "produce",
                    "example": "The factory produces over ten thousand solar panels each month.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "productivity",
                    "example": "Flexible working hours have led to a noticeable rise in employee productivity.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "productive",
                    "example": "We had a very productive brainstorming session this morning.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "productively",
                    "example": "Remote software tools allow our teams to collaborate productively from home.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Upgrading the assembly line machinery has boosted overall factory _____ by twenty percent.",
                "answer": "productivity",
                "base_word": "productive",
                "pos_hint": "danh từ",
                "vi": "Việc nâng cấp máy móc dây chuyền lắp ráp đã thúc đẩy năng suất tổng thể của nhà máy tăng hai mươi phần trăm."
            }
        },
        "satisfaction": {
            "definition_vi": "sự hài lòng, sự thỏa mãn",
            "examples_vi": [
                "Sự hài lòng của quý khách được bảo đảm, nếu không quý khách sẽ được hoàn lại tiền.",
                "Chúng tôi sẽ in ấn phẩm quảng cáo cho đến khi quý khách hài lòng."
            ],
            "collocations": [
                "customer satisfaction",
                "to sb's satisfaction",
                "job satisfaction",
                "satisfaction guaranteed"
            ],
            "usage": {
                "structures": [
                    "to one's satisfaction (đến mức ai đó hài lòng)",
                    "be satisfied with + N (hài lòng với cái gì)"
                ],
                "prepositions": ["with", "to", "of"],
                "collocations": [
                    "express satisfaction",
                    "satisfactory performance",
                    "satisfaction survey",
                    "completely satisfied"
                ],
                "tip": "Chú ý phân biệt: 'satisfied' (hài lòng - chỉ cảm xúc của người) và 'satisfactory' (thỏa đáng, đạt yêu cầu - chỉ chất lượng của sự vật/kết quả)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "satisfactorily",
                    "example": "All customer complaints must be resolved satisfactorily within 48 hours.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "If the audit results are _____, the company will proceed with the public stock offering.",
                "answer": "satisfactory",
                "base_word": "satisfaction",
                "pos_hint": "tính từ (bổ nghĩa cho sự vật/kết quả)",
                "vi": "Nếu kết quả kiểm toán đạt yêu cầu, công ty sẽ tiến hành đợt chào bán cổ phiếu ra công chúng."
            }
        }
    },
    3: {
        "characteristic": {
            "definition_vi": "đặc trưng, điển hình (adj.); đặc điểm, nét đặc thù (n.)",
            "examples_vi": [
                "Chiếc nồi nấu ăn này có những tính năng đặc trưng của thương hiệu, chẳng hạn như tay cầm 'cách nhiệt'.",
                "Một đặc điểm của cửa hàng đó là việc gửi séc hoàn tiền qua đường bưu điện rất chậm."
            ],
            "collocations": [
                "characteristic of",
                "key characteristic",
                "defining characteristic",
                "be characterized by"
            ],
            "usage": {
                "structures": [
                    "characteristic of + N (đặc trưng của cái gì)",
                    "be characterized by + N (được đặc trưng bởi)"
                ],
                "prepositions": ["of", "by"],
                "collocations": [
                    "unique characteristic",
                    "distinguishing characteristic",
                    "physical characteristics",
                    "performance characteristics"
                ],
                "tip": "Từ 'characteristic' vừa là tính từ (đi với giới từ 'of') vừa là danh từ đếm được (one characteristic / several characteristics)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "character",
                    "example": "The renovation preserved the historic character of the downtown building.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The region's economy is _____ by a strong manufacturing sector and modern port facilities.",
                "answer": "characterized",
                "base_word": "characteristic",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed - bị động)",
                "vi": "Nền kinh tế của khu vực này được đặc trưng bởi ngành sản xuất vững mạnh và cơ sở hạ tầng cảng biển hiện đại."
            }
        },
        "consequence": {
            "definition_vi": "hậu quả, hệ quả; tầm quan trọng",
            "examples_vi": [
                "Hậu quả của việc không làm theo hướng dẫn bảo dưỡng xe hơi là giấy bảo hành sẽ bị mất hiệu lực.",
                "Hệ quả của việc không đi khám nha sĩ trong nhiều năm là Lydia bị sâu răng ở vài chỗ."
            ],
            "collocations": [
                "as a consequence",
                "as a consequence of",
                "suffer the consequences",
                "serious consequences"
            ],
            "usage": {
                "structures": [
                    "as a consequence (of + N/V-ing) (= as a result of)",
                    "face / suffer / accept the consequences"
                ],
                "prepositions": ["of", "for", "to"],
                "collocations": [
                    "unintended consequences",
                    "economic consequences",
                    "of little consequence",
                    "direct consequence"
                ],
                "tip": "Cụm liên từ 'as a consequence' (= therefore: do đó) và giới từ 'as a consequence of' (= because of: do bởi) rất hay được hỏi trong Part 5 & 6."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "consequence",
                    "example": "Delayed shipments can have serious consequences for our retail partners.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "consequent",
                    "example": "The rise in fuel costs and the consequent increase in airfares hurt tourism.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "consequently",
                    "example": "The factory failed the safety inspection; consequently, production was halted.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Supply chain disruptions have persisted all quarter; _____, we must revise our delivery schedule.",
                "answer": "consequently",
                "base_word": "consequence",
                "pos_hint": "trạng từ liên kết",
                "vi": "Sự gián đoạn chuỗi cung ứng đã kéo dài suốt cả quý; do đó, chúng tôi phải điều chỉnh lại lịch giao hàng."
            }
        },
        "consider": {
            "definition_vi": "cân nhắc, xem xét kỹ; coi như, đánh giá là",
            "examples_vi": [
                "Vị khách hàng đã cân nhắc việc mua đầu đĩa DVD cho đến khi ông biết rằng phạm vi bảo hành rất hạn chế.",
                "Sau khi cân nhắc tất cả các phương án, Della quyết định mua một chiếc xe hơi đã qua sử dụng."
            ],
            "collocations": [
                "consider doing sth",
                "take into consideration",
                "under consideration",
                "considerable amount"
            ],
            "usage": {
                "structures": [
                    "consider + V-ing (cân nhắc làm gì - KHÔNG đi với to V)",
                    "consider + sb/sth + (to be) + Adj/N (coi ai/cái gì là...)"
                ],
                "prepositions": ["as", "for", "into", "under"],
                "collocations": [
                    "carefully consider",
                    "give consideration to",
                    "for your consideration",
                    "considerable expense"
                ],
                "tip": "Bẫy ngữ pháp kinh điển trong TOEIC: sau 'consider' luôn là danh từ hoặc V-ing (consider buying/expanding), tuyệt đối KHÔNG dùng 'to V'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "considerably",
                    "example": "Operating costs have decreased considerably since we switched to solar power.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The board is currently taking several relocation proposals into _____.",
                "answer": "consideration",
                "base_word": "consider",
                "pos_hint": "danh từ",
                "vi": "Hội đồng quản trị hiện đang đưa một số đề xuất di dời địa điểm vào diện xem xét."
            }
        },
        "cover": {
            "definition_vi": "bảo hiểm, chi trả (chi phí, rủi ro); bao gồm, đề cập đến; che phủ",
            "examples_vi": [
                "Bảo hiểm y tế của tôi có chi trả cho ca phẫu thuật này không?",
                "Bảo hiểm xe hơi của cô ấy cung cấp sự bảo vệ toàn diện trước rủi ro va chạm."
            ],
            "collocations": [
                "cover the cost",
                "be covered under warranty",
                "insurance coverage",
                "media coverage"
            ],
            "usage": {
                "structures": [
                    "be covered by / under + N (warranty / insurance)",
                    "cover the expenses / costs (trang trải chi phí)"
                ],
                "prepositions": ["by", "under", "against", "for"],
                "collocations": [
                    "comprehensive coverage",
                    "warranty coverage",
                    "cover a topic",
                    "cover for a colleague"
                ],
                "tip": "Danh từ 'coverage' (phạm vi bảo hiểm / việc đưa tin báo chí) là từ khóa cực kỳ quan trọng trong chủ đề Warranties & Insurance."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "cover",
                    "example": "The travel allowance is enough to cover meals and hotel accommodations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "coverage",
                    "example": "Please review your policy to ensure you have adequate liability coverage.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "covered",
                    "example": "Accidental water damage is not covered under the standard one-year warranty.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "For an additional $50, customers can purchase extended warranty _____ for up to three years.",
                "answer": "coverage",
                "base_word": "cover",
                "pos_hint": "danh từ không đếm được",
                "vi": "Với 50 đô la trả thêm, khách hàng có thể mua gói phạm vi bảo hành mở rộng lên đến ba năm."
            }
        },
        "expiration": {
            "definition_vi": "sự hết hạn, sự mãn hạn (hợp đồng, bảo hành, thực phẩm, thẻ)",
            "examples_vi": [
                "Bạn đã kiểm tra ngày hết hạn trên hộp sữa chua này chưa?",
                "Chúng ta có thể dự đoán rằng việc hết hạn hợp đồng tại Nhật Bản sẽ tác động đến doanh số bán hàng vào năm tới."
            ],
            "collocations": [
                "expiration date",
                "prior to expiration",
                "upon expiration",
                "expiration of a contract"
            ],
            "usage": {
                "structures": [
                    "expiration date (ngày hết hạn)",
                    "upon the expiration of + N (khi cái gì đó hết hạn)"
                ],
                "prepositions": ["of", "on", "upon"],
                "collocations": [
                    "warranty expiration",
                    "lease expiration",
                    "near expiration",
                    "check the expiration"
                ],
                "tip": "Cụm danh từ ghép 'expiration date' (hạn sử dụng / ngày hết hạn thẻ tín dụng, hợp đồng) xuất hiện rất đều đặn trong TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "expire",
                    "example": "Your subscription to the trade journal will expire at the end of this month.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "expiration",
                    "example": "A renewal notice is sent out thirty days before the expiration of the lease.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "expired",
                    "example": "Passengers cannot board international flights with an expired passport.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Because the promotional coupon had already _____, the cashier could not apply the discount.",
                "answer": "expired",
                "base_word": "expiration",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed)",
                "vi": "Bởi vì phiếu giảm giá khuyến mãi đã hết hạn, nhân viên thu ngân không thể áp dụng mức chiết khấu."
            }
        },
        "frequently": {
            "definition_vi": "thường xuyên, hay xảy ra",
            "examples_vi": [
                "Các thiết bị gia dụng thường đi kèm với chế độ bảo hành một năm.",
                "Chế độ bảo hành cho loại thiết bị này thường bị giới hạn về phạm vi chi trả."
            ],
            "collocations": [
                "frequently asked questions",
                "occur frequently",
                "travel frequently",
                "more frequently than"
            ],
            "usage": {
                "structures": [
                    "S + frequently + V (thường chia hiện tại đơn)",
                    "be + frequently + V3/ed (thường xuyên được...)"
                ],
                "prepositions": ["in", "with"],
                "collocations": [
                    "frequently updated",
                    "frequently used",
                    "frequent flyer",
                    "frequent inspections"
                ],
                "tip": "Giống như 'always, usually, often', trạng từ 'frequently' là dấu hiệu nhận biết của thì hiện tại đơn hoặc đứng giữa 'be' và 'V3/ed'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "frequent",
                    "example": "The café across the street is frequented by executives from our building.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "frequency",
                    "example": "The transit authority plans to increase the frequency of commuter trains.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "frequent",
                    "example": "Frequent backups are essential to prevent catastrophic data loss.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "frequently",
                    "example": "Software updates are released frequently to patch security vulnerabilities.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To reduce the _____ of mechanical breakdowns, the factory instituted weekly maintenance checks.",
                "answer": "frequency",
                "base_word": "frequently",
                "pos_hint": "danh từ",
                "vi": "Để giảm tần suất hỏng hóc máy móc, nhà máy đã thiết lập các đợt kiểm tra bảo trì hàng tuần."
            }
        },
        "imply": {
            "definition_vi": "ngụ ý, hàm ý, ám chỉ (không nói thẳng ra)",
            "examples_vi": [
                "Giấy bảo đảm trên chiếc máy nghe nhạc iPod ngụ ý rằng mọi hư hỏng đều được bảo hành trong vòng một năm.",
                "Nhân viên đại lý du lịch ám chỉ rằng khách sạn của chúng tôi không nằm ở khu vực an toàn nhất của thành phố, nhưng khi bị gặng hỏi chi tiết, anh ta lại nói vị trí đó vẫn ổn."
            ],
            "collocations": [
                "imply that",
                "implied warranty",
                "implicit agreement",
                "broad implications"
            ],
            "usage": {
                "structures": [
                    "imply + that + mệnh đề",
                    "imply + N (ngụ ý điều gì)"
                ],
                "prepositions": ["in", "by", "from"],
                "collocations": [
                    "financial implications",
                    "strongly imply",
                    "implicit trust",
                    "implied consent"
                ],
                "tip": "Danh từ 'implication(s)' trong TOEIC thường mang nghĩa 'hệ lụy / tác động kéo theo' (VD: financial/legal implications)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "implicitly",
                    "example": "The manager trusts her assistant implicitly to handle confidential files.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The committee is carefully studying the financial _____ of the new tax legislation.",
                "answer": "implications",
                "base_word": "imply",
                "pos_hint": "danh từ số nhiều",
                "vi": "Ủy ban đang nghiên cứu kỹ lưỡng những tác động/hệ lụy tài chính của đạo luật thuế mới."
            }
        },
        "promise": {
            "definition_vi": "lời hứa, sự cam kết (n.); hứa hẹn, cam kết (v.)",
            "examples_vi": [
                "Bảo hành là một lời cam kết mà nhà sản xuất đưa ra cho người tiêu dùng.",
                "Nhân viên bán hàng đã hứa rằng chiếc nệm mới của chúng tôi sẽ được giao đến trước buổi trưa thứ Bảy."
            ],
            "collocations": [
                "make a promise",
                "keep a promise",
                "promise to do",
                "promising career"
            ],
            "usage": {
                "structures": [
                    "promise + (sb) + to V / that + mệnh đề",
                    "make / keep / break / fulfill a promise"
                ],
                "prepositions": ["to", "of"],
                "collocations": [
                    "show great promise",
                    "promising results",
                    "solemn promise",
                    "empty promise"
                ],
                "tip": "Tính từ 'promising' (đầy hứa hẹn, có triển vọng) rất hay được dùng để khen ngợi ứng viên (promising candidate) hoặc kết quả (promising results)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "promise",
                    "example": "The contractor promised to finish the remodeling project by November.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "promise",
                    "example": "The new solar battery technology shows tremendous commercial promise.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "promising",
                    "example": "Initial clinical trials of the medication have yielded very promising results.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "promisingly",
                    "example": "The fiscal year began promisingly with record sales in January.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Among the interns hired this summer, Ms. Patel has shown the most _____ future as an analyst.",
                "answer": "promising",
                "base_word": "promise",
                "pos_hint": "tính từ",
                "vi": "Trong số các thực tập sinh được tuyển dụng vào mùa hè này, cô Patel đã cho thấy tương lai đầy triển vọng nhất ở vị trí nhà phân tích."
            }
        },
        "protect": {
            "definition_vi": "bảo vệ, che chở, giữ an toàn",
            "examples_vi": [
                "Luật bảo vệ người tiêu dùng được thiết kế để bảo vệ công chúng trước những người bán hàng gian dối.",
                "Bạn có thể tự bảo vệ mình khỏi các trò lừa đảo bằng cách tìm hiểu thông tin chi tiết về người bán."
            ],
            "collocations": [
                "protect against / from",
                "consumer protection",
                "protective gear",
                "data protection"
            ],
            "usage": {
                "structures": [
                    "protect + sb/sth + from / against + N",
                    "offer / provide protection against + N"
                ],
                "prepositions": ["from", "against", "under"],
                "collocations": [
                    "protective clothing",
                    "environmental protection",
                    "patent protection",
                    "protective eyewear"
                ],
                "tip": "Luôn nhớ cặp giới từ đi kèm với 'protect/protection' là 'from' hoặc 'against' (bảo vệ khỏi cái gì)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "protectively",
                    "example": "Fragile ceramic items must be wrapped protectively before shipping.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All laboratory technicians are required to wear _____ gloves and goggles when handling chemicals.",
                "answer": "protective",
                "base_word": "protect",
                "pos_hint": "tính từ",
                "vi": "Tất cả các kỹ thuật viên phòng thí nghiệm được yêu cầu phải đeo găng tay và kính bảo hộ khi tiếp xúc với hóa chất."
            }
        },
        "reputation": {
            "definition_vi": "danh tiếng, uy tín, tiếng tăm",
            "examples_vi": [
                "Mặc dù nhân viên bán hàng giới thiệu cho tôi một sản phẩm mà tôi chưa từng nghe đến, tôi vẫn mua nó vì uy tín tốt đẹp của nhà sản xuất.",
                "Công ty hiểu rằng uy tín của các sản phẩm chính là tài sản quan trọng nhất mà họ có được."
            ],
            "collocations": [
                "earn a reputation",
                "reputation for quality",
                "reputable company",
                "damage a reputation"
            ],
            "usage": {
                "structures": [
                    "have / build / earn a reputation for + N/V-ing",
                    "live up to one's reputation (xứng đáng với danh tiếng)"
                ],
                "prepositions": ["for", "as", "of"],
                "collocations": [
                    "solid reputation",
                    "tarnish a reputation",
                    "reputable dealer",
                    "international reputation"
                ],
                "tip": "Danh từ 'reputation' đi với giới từ 'for' (reputation for reliability: uy tín về sự đáng tin cậy); tính từ 'reputable' có nghĩa là 'có uy tín, đáng tin cậy'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "repute",
                    "example": "The antique vase is reputed to be over three hundred years old.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "reputably",
                    "example": "Always purchase replacement parts from a reputably certified dealer.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Before signing a home renovation contract, make sure you are dealing with a _____ builder.",
                "answer": "reputable",
                "base_word": "reputation",
                "pos_hint": "tính từ",
                "vi": "Trước khi ký hợp đồng cải tạo nhà, hãy chắc chắn rằng bạn đang làm việc với một nhà thầu có uy tín."
            }
        },
        "require": {
            "definition_vi": "yêu cầu, đòi hỏi, bắt buộc",
            "examples_vi": [
                "Bảo hành xe hơi có thể yêu cầu chủ sở hữu phải đưa xe đi bảo dưỡng bởi một thợ máy có chứng chỉ.",
                "Luật pháp yêu cầu mỗi mặt hàng phải hiển thị rõ ràng thông tin bảo hành."
            ],
            "collocations": [
                "be required to do",
                "meet the requirements",
                "require that + S + V(bare)",
                "minimum requirement"
            ],
            "usage": {
                "structures": [
                    "require + sb + to V / passive: be required to V",
                    "require + that + S + (should) + V nguyên mẫu (thức giả định)"
                ],
                "prepositions": ["of", "for", "by"],
                "collocations": [
                    "legal requirement",
                    "safety requirements",
                    "requisite skills",
                    "strictly required"
                ],
                "tip": "Trong mệnh đề 'require that + S + V', động từ phía sau luôn ở dạng nguyên mẫu không chia (VD: The law requires that every item display...)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "required",
                    "example": "Please fill out all required fields on the online registration form.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Applicants who do not meet the minimum _____ for the position will not be called for an interview.",
                "answer": "requirements",
                "base_word": "require",
                "pos_hint": "danh từ số nhiều",
                "vi": "Những ứng viên không đáp ứng được các yêu cầu tối thiểu cho vị trí này sẽ không được gọi phỏng vấn."
            }
        },
        "variety": {
            "definition_vi": "sự đa dạng, nhiều thứ khác nhau; chủng loại",
            "examples_vi": [
                "Có rất nhiều điều khoản tiêu chuẩn khác nhau mà bạn sẽ bắt gặp trong các giấy bảo hành.",
                "Hàng loạt vấn đề không lường trước đã xuất hiện sau khi sản phẩm được tung ra thị trường khoảng sáu tháng."
            ],
            "collocations": [
                "a wide variety of",
                "a great variety of",
                "for a variety of reasons",
                "offer variety"
            ],
            "usage": {
                "structures": [
                    "a (wide / great / large) variety of + N số nhiều",
                    "vary from A to B (dao động/khác nhau từ A đến B)"
                ],
                "prepositions": ["of", "in"],
                "collocations": [
                    "endless variety",
                    "various options",
                    "vary widely",
                    "varied experience"
                ],
                "tip": "Cụm lượng từ 'a (wide) variety of + danh từ số nhiều' (= various + danh từ số nhiều) là một trong những cụm xuất hiện nhiều nhất trong TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "vary",
                    "example": "Shipping charges vary depending on the weight and destination of the package.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "variety",
                    "example": "The department store carries a wide variety of imported kitchenware.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "various",
                    "example": "We interviewed various candidates before selecting the new branch manager.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "variously",
                    "example": "The project's cost has been variously estimated at between two and five million dollars.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Hotel room rates _____ significantly depending on the season and length of stay.",
                "answer": "vary",
                "base_word": "variety",
                "pos_hint": "động từ nguyên mẫu (chủ ngữ số nhiều)",
                "vi": "Giá phòng khách sạn thay đổi đáng kể tùy thuộc vào mùa và thời gian lưu trú."
            }
        }
    },
    4: {
        "address": {
            "definition_vi": "giải quyết, xử lý (vấn đề, nhu cầu) (v.); bài diễn văn trang trọng; địa chỉ (n.)",
            "examples_vi": [
                "Bài báo đã ca ngợi bài phát biểu của bà trước ban chỉ đạo.",
                "Kế hoạch kinh doanh của Marco giải quyết đúng những nhu cầu của các chủ doanh nghiệp nhỏ."
            ],
            "collocations": [
                "address an issue",
                "address the needs of",
                "deliver an address",
                "keynote address"
            ],
            "usage": {
                "structures": [
                    "address + a problem / concern / issue / need (giải quyết vấn đề/nhu cầu)",
                    "deliver / give an address to + sb (phát biểu trước ai)"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "opening address",
                    "address customer complaints",
                    "return address",
                    "address the audience"
                ],
                "tip": "Trong TOEIC, ngoài nghĩa 'địa chỉ', 'address' rất hay là động từ mang nghĩa 'giải quyết' (= deal with/resolve) hoặc danh từ mang nghĩa 'bài phát biểu' (= speech)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "address",
                    "example": "The task force was formed to address the decline in employee morale.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "addressee",
                    "example": "If the addressee is no longer at this location, please return the letter to the sender.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "addressable",
                    "example": "Most of the software bugs reported by beta testers are easily addressable.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The CEO's keynote _____ at the annual shareholder meeting focused on sustainable growth.",
                "answer": "address",
                "base_word": "address",
                "pos_hint": "danh từ số ít (bài diễn văn)",
                "vi": "Bài phát biểu chính của vị giám đốc điều hành tại cuộc họp cổ đông thường niên tập trung vào sự tăng trưởng bền vững."
            }
        },
        "avoid": {
            "definition_vi": "tránh, ngăn ngừa không cho xảy ra",
            "examples_vi": [
                "Để tránh bị phá sản, các chủ sở hữu nên chuẩn bị một bản kế hoạch kinh doanh bài bản.",
                "Những sai sót trong kế toán của Lloyd lẽ ra đã có thể tránh được nhờ một buổi tư vấn kinh doanh với nhân viên ngân hàng của anh ấy."
            ],
            "collocations": [
                "avoid making mistakes",
                "avoid delays",
                "tax avoidance",
                "avoidable error"
            ],
            "usage": {
                "structures": [
                    "avoid + N / V-ing (tránh làm gì - KHÔNG đi với to V)"
                ],
                "prepositions": ["by", "from"],
                "collocations": [
                    "avoid conflict",
                    "avoid traffic congestion",
                    "strictly avoid",
                    "unavoidable delay"
                ],
                "tip": "Giống như 'consider', sau động từ 'avoid' nếu là động từ thì bắt buộc phải chia ở dạng danh động từ V-ing (avoid going, avoid paying)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "avoidable",
                    "example": "Many workplace injuries are completely avoidable if safety rules are followed.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "avoidably",
                    "example": "Several shipments were avoidably delayed due to incomplete customs forms.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Your _____ of these financial issues will only make the situation worse in the long run.",
                "answer": "avoidance",
                "base_word": "avoid",
                "pos_hint": "danh từ",
                "vi": "Việc bạn né tránh những vấn đề tài chính này sẽ chỉ làm cho tình hình trở nên tồi tệ hơn về lâu dài."
            }
        },
        "demonstrate": {
            "definition_vi": "chứng minh, thể hiện rõ; trình diễn, hướng dẫn thực hành (cách dùng sản phẩm)",
            "examples_vi": [
                "Kế hoạch kinh doanh của Alban đã chứng minh rằng anh ấy đã suy tính rất nhiều để biến ước mơ của mình thành hiện thực.",
                "Vị giáo sư đã chứng minh thông qua một nghiên cứu tình huống rằng một kế hoạch kinh doanh có thể gây ấn tượng với bên cho vay."
            ],
            "collocations": [
                "demonstrate how to",
                "product demonstration",
                "clearly demonstrate",
                "demonstrate leadership"
            ],
            "usage": {
                "structures": [
                    "demonstrate + N / that + mệnh đề / how to V",
                    "give / hold a demonstration of + N"
                ],
                "prepositions": ["to", "by", "through"],
                "collocations": [
                    "live demonstration",
                    "demonstrate commitment",
                    "demonstrate proficiency",
                    "cooking demonstration"
                ],
                "tip": "Danh từ 'demonstration' (buổi giới thiệu/trình diễn sản phẩm trực tiếp) rất hay xuất hiện trong các thông báo triển lãm thương mại (trade show)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "demonstratively",
                    "example": "The audience applauded demonstratively at the end of the product launch.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Visitors to booth 14 can watch a live _____ of our latest robotic vacuum cleaner.",
                "answer": "demonstration",
                "base_word": "demonstrate",
                "pos_hint": "danh từ số ít",
                "vi": "Khách tham quan tại gian hàng số 14 có thể xem một màn trình diễn trực tiếp mẫu robot hút bụi mới nhất của chúng tôi."
            }
        },
        "develop": {
            "definition_vi": "phát triển, mở rộng, xây dựng (ý tưởng, sản phẩm, kế hoạch)",
            "examples_vi": [
                "Lily đã phát triển các ý tưởng của mình thành một bản kế hoạch kinh doanh bằng cách tham gia một lớp học tại trường cao đẳng cộng đồng.",
                "Nhà hàng mà Wanda mở mười năm trước đã phát triển thành một chuỗi cửa hàng trên toàn quốc."
            ],
            "collocations": [
                "develop a plan",
                "research and development",
                "software developer",
                "develop into"
            ],
            "usage": {
                "structures": [
                    "develop (A) into B (phát triển thành cái gì)",
                    "be under development (đang trong quá trình phát triển)"
                ],
                "prepositions": ["into", "from", "under"],
                "collocations": [
                    "career development",
                    "real estate developer",
                    "developing countries",
                    "recent developments"
                ],
                "tip": "Cụm giới từ 'under development' (đang được phát triển/xây dựng) là cụm cố định rất hay được hỏi trong Part 5."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "developed",
                    "example": "Our newly developed battery lasts twice as long as previous models.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The pharmaceutical company currently has three promising new vaccines under _____.",
                "answer": "development",
                "base_word": "develop",
                "pos_hint": "danh từ",
                "vi": "Công ty dược phẩm hiện đang có ba loại vắc-xin mới đầy triển vọng nằm trong quá trình phát triển."
            }
        },
        "evaluate": {
            "definition_vi": "đánh giá, định giá, thẩm định",
            "examples_vi": [
                "Điều quan trọng là phải đánh giá các đối thủ cạnh tranh của bạn khi lập một kế hoạch kinh doanh.",
                "Các bên cho vay đã thẩm định mức độ uy tín tín dụng của chúng tôi và quyết định cho chúng tôi vay tiền."
            ],
            "collocations": [
                "evaluate performance",
                "annual evaluation",
                "evaluate the impact",
                "carefully evaluate"
            ],
            "usage": {
                "structures": [
                    "evaluate + N / wh-clause",
                    "conduct / perform an evaluation of + N"
                ],
                "prepositions": ["by", "on", "of"],
                "collocations": [
                    "performance evaluation",
                    "independent evaluator",
                    "risk evaluation",
                    "thorough evaluation"
                ],
                "tip": "Cụm danh từ ghép 'performance evaluation' (đánh giá năng lực làm việc của nhân viên) xuất hiện cực kỳ phổ biến trong chủ đề Nhân sự (Personnel)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "evaluative",
                    "example": "The consultant used several evaluative criteria to rank the suppliers.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Every employee receives a formal performance _____ at the end of the fiscal year.",
                "answer": "evaluation",
                "base_word": "evaluate",
                "pos_hint": "danh từ số ít",
                "vi": "Mỗi nhân viên đều nhận được một bản đánh giá năng lực làm việc chính thức vào cuối năm tài chính."
            }
        },
        "gather": {
            "definition_vi": "thu thập, tập hợp (thông tin, dữ liệu, con người); suy ra, hiểu rằng",
            "examples_vi": [
                "Chúng tôi đã thu thập thông tin cho kế hoạch của mình từ nhiều nguồn khác nhau.",
                "Tôi suy đoán rằng lãi suất dành cho các doanh nghiệp nhỏ sẽ sớm thay đổi."
            ],
            "collocations": [
                "gather information",
                "gather data",
                "gather together",
                "social gathering"
            ],
            "usage": {
                "structures": [
                    "gather + N (information / data / evidence) (from + N)",
                    "gather + (that) + mệnh đề (suy ra/hiểu rằng)"
                ],
                "prepositions": ["from", "around", "in"],
                "collocations": [
                    "gather feedback",
                    "gather support",
                    "informal gathering",
                    "gather momentum"
                ],
                "tip": "Danh từ 'gathering' không mang nghĩa 'sự thu thập' mà thường chỉ một 'buổi tụ họp/cuộc gặp gỡ đông người' (a social/family gathering)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "gather",
                    "example": "Researchers gathered survey responses from over two thousand commuters.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "gathering",
                    "example": "The resort is an ideal venue for corporate retreats and large gatherings.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "gathered",
                    "example": "The CEO thanked the gathered journalists for attending the press conference.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The botanical garden's glass pavilion can be rented for weddings and corporate _____.",
                "answer": "gatherings",
                "base_word": "gather",
                "pos_hint": "danh từ số nhiều",
                "vi": "Nhà vòm bằng kính của vườn bách thảo có thể được thuê để tổ chức đám cưới và các buổi tụ họp doanh nghiệp."
            }
        },
        "offer": {
            "definition_vi": "lời đề nghị, ưu đãi (n.); đề nghị, cung cấp, đưa ra (v.)",
            "examples_vi": [
                "Devon đã chấp nhận lời đề nghị viết bản kế hoạch kinh doanh của chúng tôi.",
                "Jackie phải cung cấp cho nhân viên ngân hàng những số liệu thống kê mới để khuyến khích ngân hàng cho cô vay tiền khởi nghiệp."
            ],
            "collocations": [
                "job offer",
                "special offer",
                "make an offer",
                "offer a discount"
            ],
            "usage": {
                "structures": [
                    "offer + to V (đề nghị/tự nguyện làm gì)",
                    "offer + sb + sth / offer + sth + to sb",
                    "accept / decline / make an offer"
                ],
                "prepositions": ["to", "for", "on"],
                "collocations": [
                    "promotional offer",
                    "limited-time offer",
                    "generous offer",
                    "course offerings"
                ],
                "tip": "Danh từ phái sinh 'offering(s)' thường dùng ở số nhiều để chỉ 'các sản phẩm/dịch vụ/khóa học được cung cấp' (product/course offerings)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "offer",
                    "example": "The store offers free home delivery on orders over a hundred dollars.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "offering",
                    "example": "The university has expanded its online course offerings this semester.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To remain competitive, the bakery is adding several gluten-free pastries to its daily _____.",
                "answer": "offerings",
                "base_word": "offer",
                "pos_hint": "danh từ số nhiều (các mặt hàng được cung cấp)",
                "vi": "Để duy trì sức cạnh tranh, tiệm bánh đang bổ sung một số loại bánh ngọt không chứa gluten vào danh mục sản phẩm hàng ngày của mình."
            }
        },
        "primarily": {
            "definition_vi": "chủ yếu, trước hết, quan trọng nhất",
            "examples_vi": [
                "Mối quan tâm hàng đầu của chúng tôi là thuyết phục hội đồng quản trị nộp đơn xin khoản vay thứ hai.",
                "Các nhà phát triển đang suy nghĩ chủ yếu về cách thức thâm nhập thị trường Nam Mỹ."
            ],
            "collocations": [
                "primarily responsible for",
                "consist primarily of",
                "primarily concerned with",
                "aimed primarily at"
            ],
            "usage": {
                "structures": [
                    "be + primarily + V3/ed / Adj + Prep (designed for / aimed at / responsible for)",
                    "primarily + giới từ (primarily because of / primarily for)"
                ],
                "prepositions": ["for", "with", "of", "at"],
                "collocations": [
                    "primarily intended for",
                    "focus primarily on",
                    "primary objective",
                    "primary reason"
                ],
                "tip": "Trạng từ 'primarily' (= mainly / chiefly) rất hay đứng giữa động từ to be và phân từ quá khứ hoặc trước một cụm giới từ để nhấn mạnh."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "primacy",
                    "example": "The company's success is built on the primacy of customer satisfaction.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "primary",
                    "example": "Our primary goal this quarter is to reduce manufacturing defects.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "primarily",
                    "example": "The seminar is designed primarily for newly appointed team leaders.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The _____ reason for relocating our warehouse is to be closer to the main highway.",
                "answer": "primary",
                "base_word": "primarily",
                "pos_hint": "tính từ",
                "vi": "Lý do chính của việc di dời nhà kho của chúng tôi là để ở gần đường cao tốc chính hơn."
            }
        },
        "risk": {
            "definition_vi": "rủi ro, nguy cơ tổn thất (n.); liều lĩnh, mạo hiểm (v.)",
            "examples_vi": [
                "Rủi ro hàng đầu đối với hầu hết các doanh nghiệp mới khởi nghiệp là thiếu vốn.",
                "Việc mở rộng sang một thị trường mới là một sự mạo hiểm lớn."
            ],
            "collocations": [
                "take a risk",
                "at risk of",
                "minimize risk",
                "financial risk"
            ],
            "usage": {
                "structures": [
                    "risk + V-ing (mạo hiểm làm gì - KHÔNG đi với to V)",
                    "at the risk of + N/V-ing (với nguy cơ...)"
                ],
                "prepositions": ["of", "at", "to"],
                "collocations": [
                    "risk management",
                    "high-risk investment",
                    "pose a risk to",
                    "run the risk of"
                ],
                "tip": "Khi là động từ, sau 'risk' bắt buộc dùng V-ing (risk losing money: có nguy cơ mất tiền)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "risk",
                    "example": "Companies that ignore market research risk losing their competitive edge.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "risk",
                    "example": "Diversifying your portfolio helps reduce overall investment risk.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "risky",
                    "example": "Launching an untested product nationwide is a very risky strategy.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "riskily",
                    "example": "The hedge fund invested too riskily in volatile tech startups.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Analysts warned that investing all of the firm's capital in a single venture would be too _____.",
                "answer": "risky",
                "base_word": "risk",
                "pos_hint": "tính từ",
                "vi": "Các nhà phân tích đã cảnh báo rằng việc đầu tư toàn bộ vốn của công ty vào một dự án duy nhất sẽ là quá mạo hiểm."
            }
        },
        "strategy": {
            "definition_vi": "chiến lược, kế hoạch hành động",
            "examples_vi": [
                "Một bản kế hoạch kinh doanh là một chiến lược để điều hành doanh nghiệp và tránh các rắc rối.",
                "Chúng ta hãy xây dựng một chiến lược để quảng bá cho tiệm kem của mình."
            ],
            "collocations": [
                "marketing strategy",
                "develop a strategy",
                "long-term strategy",
                "strategic alliance"
            ],
            "usage": {
                "structures": [
                    "strategy for + V-ing / N",
                    "strategy + to V"
                ],
                "prepositions": ["for", "to"],
                "collocations": [
                    "business strategy",
                    "pricing strategy",
                    "strategic planning",
                    "implement a strategy"
                ],
                "tip": "Tính từ 'strategic' rất hay đứng trước các danh từ như 'plan, partnership, alliance, location, decision'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "strategically",
                    "example": "Our new distribution center is strategically located near the international airport.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The hotel is _____ located within walking distance of the city's main convention center.",
                "answer": "strategically",
                "base_word": "strategy",
                "pos_hint": "trạng từ",
                "vi": "Khách sạn nằm ở một vị trí mang tính chiến lược, chỉ cách trung tâm hội nghị chính của thành phố vài bước chân."
            }
        },
        "strong": {
            "definition_vi": "mạnh mẽ, thuyết phục; vững mạnh (về kinh tế, tài chính)",
            "examples_vi": [
                "Vị giáo sư đã đưa ra một lập luận đanh thép về giá trị của một bản kế hoạch kinh doanh tốt.",
                "Ngay cả trong một môi trường kinh tế vững mạnh thì nhiều doanh nghiệp vẫn thất bại, vì vậy hãy lập kế hoạch thật cẩn thận."
            ],
            "collocations": [
                "strong economy",
                "strong argument",
                "strong demand",
                "strengthen ties"
            ],
            "usage": {
                "structures": [
                    "strong + N (support / demand / growth / performance)",
                    "strengthen + N (củng cố, tăng cường cái gì)"
                ],
                "prepositions": ["in", "on"],
                "collocations": [
                    "strong commitment",
                    "strong candidate",
                    "financial strength",
                    "strongly recommend"
                ],
                "tip": "Chú ý họ từ bất quy tắc của 'strong (adj)': danh từ là 'strength' (sức mạnh/điểm mạnh) và động từ là 'strengthen' (củng cố/tăng cường)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "strengthen",
                    "example": "The trade agreement is expected to strengthen economic ties between the two nations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "strength",
                    "example": "One of the candidate's greatest strengths is her fluency in three languages.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "strong",
                    "example": "Strong consumer demand drove fourth-quarter profits to a record high.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "strongly",
                    "example": "We strongly advise passengers to arrive at the airport two hours early.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Acquiring the local software firm will significantly _____ our position in the Asian market.",
                "answer": "strengthen",
                "base_word": "strong",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Việc mua lại công ty phần mềm địa phương sẽ củng cố đáng kể vị thế của chúng ta tại thị trường châu Á."
            }
        },
        "substitution": {
            "definition_vi": "sự thay thế, sự đổi chỗ",
            "examples_vi": [
                "Việc bạn thay thế tên giả cho tên thật khiến tài liệu có vẻ thiếu chân thực.",
                "Không có gì có thể thay thế được cho sự làm việc chăm chỉ và lòng kiên trì."
            ],
            "collocations": [
                "substitution of A for B",
                "no substitution for",
                "substitute for",
                "make a substitution"
            ],
            "usage": {
                "structures": [
                    "substitute A for B (dùng A để thay thế cho B)",
                    "substitute for + B (thay thế cho B)"
                ],
                "prepositions": ["for", "of"],
                "collocations": [
                    "ingredient substitution",
                    "find a substitute",
                    "substitute teacher",
                    "without substitution"
                ],
                "tip": "Giới từ đi kèm với cả danh từ và động từ 'substitute / substitution' luôn là 'for' (substitute A for B = dùng A thay cho B)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "substitutable",
                    "example": "In this recipe, maple syrup is easily substitutable for honey.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "If the requested item is out of stock, we will _____ a product of equal or greater value.",
                "answer": "substitute",
                "base_word": "substitution",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Nếu mặt hàng được yêu cầu đã hết trong kho, chúng tôi sẽ thay thế bằng một sản phẩm có giá trị tương đương hoặc lớn hơn."
            }
        }
    },
    5: {
        "accommodate": {
            "definition_vi": "có đủ chỗ chứa; đáp ứng (nhu cầu, yêu cầu); cung cấp chỗ ở",
            "examples_vi": [
                "Phòng họp đủ rộng để đáp ứng các nhu cầu đa dạng của những nhóm sử dụng nó.",
                "Bởi vì hạn chót đặt phòng đã qua, quản lý khách sạn không thể đáp ứng nhu cầu thêm phòng của chúng tôi."
            ],
            "collocations": [
                "accommodate guests",
                "accommodate a request",
                "hotel accommodations",
                "accommodating staff"
            ],
            "usage": {
                "structures": [
                    "accommodate + N (number of people / needs / requests / changes)",
                    "make accommodations for + N"
                ],
                "prepositions": ["with", "for"],
                "collocations": [
                    "comfortably accommodate",
                    "overnight accommodations",
                    "accommodate special dietary needs",
                    "seating capacity to accommodate"
                ],
                "tip": "Trong TOEIC, 'accommodate' có 2 nghĩa cực kỳ phổ biến: (1) chứa được bao nhiêu người (Grand Ballroom can accommodate 300 guests), (2) đáp ứng yêu cầu (accommodate your request/schedule)."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "accommodatingly",
                    "example": "The receptionist accommodatingly offered to store our luggage until check-in time.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Conference registration fees include all workshop materials, meals, and hotel _____.",
                "answer": "accommodations",
                "base_word": "accommodate",
                "pos_hint": "danh từ số nhiều (chỗ ăn ở)",
                "vi": "Lệ phí đăng ký hội nghị đã bao gồm tất cả tài liệu hội thảo, các bữa ăn và chỗ ở tại khách sạn."
            }
        },
        "arrangement": {
            "definition_vi": "sự sắp xếp, sự thu xếp (thường dùng ở số nhiều cho công tác chuẩn bị); cách bố trí",
            "examples_vi": [
                "Việc thu xếp chuyến công tác đã được Sara, trợ lý đắc lực của ông Billings, lo liệu chu đáo.",
                "Thứ tự sắp xếp các diễn giả được tính theo bảng chữ cái để tránh làm mất lòng bất kỳ ai."
            ],
            "collocations": [
                "make arrangements for",
                "travel arrangements",
                "seating arrangement",
                "prior arrangement"
            ],
            "usage": {
                "structures": [
                    "make arrangements (for + N / to V) (thu xếp cho việc gì)",
                    "arrange (for sb) to V"
                ],
                "prepositions": ["for", "with", "of"],
                "collocations": [
                    "flower arrangement",
                    "financial arrangement",
                    "flexible work arrangements",
                    "finalize the arrangements"
                ],
                "tip": "Khi mang nghĩa 'công tác chuẩn bị/thu xếp' (như đặt vé, đặt phòng), 'arrangements' luôn dùng ở dạng số nhiều và đi với động từ 'make' (make travel arrangements)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "arranger",
                    "example": "We hired a professional floral arranger to decorate the banquet hall.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Please contact the human resources office to _____ a convenient time for your orientation.",
                "answer": "arrange",
                "base_word": "arrangement",
                "pos_hint": "động từ nguyên mẫu",
                "vi": "Vui lòng liên hệ với văn phòng nhân sự để sắp xếp một thời gian thuận tiện cho buổi định hướng của bạn."
            }
        },
        "association": {
            "definition_vi": "hiệp hội, tổ chức nghề nghiệp; sự liên kết, mối quan hệ hợp tác",
            "examples_vi": [
                "Tư cách thành viên trong một hiệp hội thương mại hoặc nghề nghiệp mang lại các mối quan hệ kinh doanh và sự hỗ trợ lẫn nhau.",
                "Các công ty điện thoại địa phương đã thành lập một hiệp hội để phục vụ các mục tiêu chung, đáp ứng nhu cầu chung và nâng cao hiệu quả."
            ],
            "collocations": [
                "trade association",
                "in association with",
                "professional association",
                "be associated with"
            ],
            "usage": {
                "structures": [
                    "in association with + N (hợp tác/phối hợp cùng với)",
                    "be associated with + N (có liên quan đến)"
                ],
                "prepositions": ["with", "in", "of"],
                "collocations": [
                    "alumni association",
                    "close association",
                    "form an association",
                    "sales associate"
                ],
                "tip": "Chú ý từ 'associate' ngoài làm động từ (liên kết) còn là danh từ chỉ người rất phổ biến trong TOEIC: 'sales associate' (nhân viên bán hàng) hoặc 'business associate' (đồng nghiệp/đối tác)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "associate",
                    "example": "A polite sales associate helped me find the right size jacket.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The charity concert is being organized in _____ with several local businesses.",
                "answer": "association",
                "base_word": "association",
                "pos_hint": "danh từ",
                "vi": "Buổi hòa nhạc từ thiện đang được tổ chức với sự phối hợp của một số doanh nghiệp địa phương."
            }
        },
        "attend": {
            "definition_vi": "tham dự, có mặt tại (cuộc họp, sự kiện); chú tâm, chăm sóc, giải quyết (đi với 'to')",
            "examples_vi": [
                "Chúng tôi dự kiến có hơn 100 thành viên sẽ tham dự cuộc họp thường niên.",
                "Người quản lý khách sạn đã giải quyết chu đáo mọi nhu cầu của chúng tôi một cách nhanh chóng."
            ],
            "collocations": [
                "attend a conference",
                "attend to a matter",
                "conference attendees",
                "high attendance"
            ],
            "usage": {
                "structures": [
                    "attend + N (meeting / seminar / class) (tham dự - KHÔNG có giới từ)",
                    "attend to + N (chăm sóc, xử lý, giải quyết việc gì)"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "in attendance",
                    "flight attendant",
                    "attendance record",
                    "mandatory attendance"
                ],
                "tip": "Bẫy kinh điển trong Part 5: phân biệt 2 danh từ 'attendance' (sự tham dự/sĩ số người có mặt - không đếm được) và 'attendee' (người tham dự - đếm được)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "attentive",
                    "example": "The restaurant received glowing reviews for its delicious food and attentive staff.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "attentively",
                    "example": "The trainees listened attentively as the instructor explained the safety protocol.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All conference _____ will receive a name badge and a welcome packet at the registration desk.",
                "answer": "attendees",
                "base_word": "attend",
                "pos_hint": "danh từ chỉ người số nhiều",
                "vi": "Tất cả những người tham dự hội nghị sẽ nhận được bảng tên và bộ tài liệu chào mừng tại bàn đăng ký."
            }
        },
        "get in touch": {
            "definition_vi": "liên lạc, giữ liên hệ với (ai đó)",
            "examples_vi": [
                "Ngay khi đến khách sạn, chúng tôi sẽ liên lạc với người quản lý về những vị khách phát sinh ngoài dự kiến.",
                "Quầy đăng ký là một vị trí trung tâm thuận lợi để mọi người liên lạc với nhau."
            ],
            "collocations": [
                "get in touch with",
                "stay in touch",
                "keep in touch",
                "be in touch with"
            ],
            "usage": {
                "structures": [
                    "get / keep / stay / be in touch (with + sb)"
                ],
                "prepositions": ["with"],
                "collocations": [
                    "lose touch with",
                    "put sb in touch with",
                    "closely in touch",
                    "get back in touch"
                ],
                "tip": "Cụm 'get in touch with sb' hoàn toàn đồng nghĩa với 'contact sb' (nhưng lưu ý: 'contact' không có giới từ 'with', còn 'get in touch' bắt buộc có 'with')."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "touch",
                    "example": "Visitors are asked not to touch the paintings on display in the gallery.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "touch",
                    "example": "Adding fresh flowers gave the hotel lobby a welcoming personal touch.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "touching",
                    "example": "The retiring director gave a touching farewell speech to her staff.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "touchingly",
                    "example": "He spoke touchingly about the mentors who guided his early career.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "A customer service representative will get in _____ with you within 24 hours to resolve your issue.",
                "answer": "touch",
                "base_word": "get in touch",
                "pos_hint": "danh từ (trong cụm cố định)",
                "vi": "Một đại diện dịch vụ khách hàng sẽ liên lạc với bạn trong vòng 24 giờ để giải quyết vấn đề của bạn."
            }
        },
        "hold": {
            "definition_vi": "tổ chức, tiến hành (cuộc họp, sự kiện); có sức chứa; nắm giữ (vị trí, cổ phần)",
            "examples_vi": [
                "Phòng họp này có thể chứa thoải mái ít nhất 80 người.",
                "Cô ấy tổ chức một buổi hội thảo thường niên rất được ưa chuộng."
            ],
            "collocations": [
                "hold a meeting",
                "hold a conference",
                "hold a position",
                "put on hold"
            ],
            "usage": {
                "structures": [
                    "hold + N (meeting / event / election / seminar) (tổ chức)",
                    "hold + số lượng + people/guests (có sức chứa bao nhiêu người)",
                    "hold + sb + responsible/accountable for (quy trách nhiệm cho ai)"
                ],
                "prepositions": ["on", "in", "up"],
                "collocations": [
                    "hold accountable",
                    "on hold",
                    "shareholder",
                    "hold talks"
                ],
                "tip": "Quá khứ và phân từ 2 của 'hold' là 'held'; cấu trúc bị động 'be held at/in + địa điểm / on + ngày' (được tổ chức tại/vào...) xuất hiện trong hầu như mọi đề thi TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "hold",
                    "example": "The board of directors holds its quarterly meeting on the first Monday of the month.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "holder",
                    "example": "Season ticket holders are eligible for a 20 percent discount on merchandise.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "holding",
                    "example": "The corporation expanded its real estate holdings across the Midwest.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "This year's international trade fair will be _____ at the Harbor Convention Center in May.",
                "answer": "held",
                "base_word": "hold",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed - bị động)",
                "vi": "Hội chợ thương mại quốc tế năm nay sẽ được tổ chức tại Trung tâm Hội nghị Cảng vào tháng Năm."
            }
        },
        "location": {
            "definition_vi": "địa điểm, vị trí, cơ sở/chi nhánh",
            "examples_vi": [
                "Địa điểm của cuộc họp đã được đổi từ Phòng Đỏ sang Phòng Xanh.",
                "Disney World là địa điểm hoàn hảo cho cuộc họp thường niên vì nhiều thành viên có thể đưa gia đình đi cùng."
            ],
            "collocations": [
                "central location",
                "convenient location",
                "prime location",
                "retail locations"
            ],
            "usage": {
                "structures": [
                    "be located in / at / near + địa điểm (tọa lạc tại)",
                    "relocate to + địa điểm (chuyển địa điểm đến)"
                ],
                "prepositions": ["of", "in", "at", "on"],
                "collocations": [
                    "ideal location",
                    "branch location",
                    "undisclosed location",
                    "on location"
                ],
                "tip": "Cấu trúc 'be conveniently/centrally located' (nằm ở vị trí thuận tiện/trung tâm) là câu mẫu kinh điển để mô tả khách sạn hoặc văn phòng trong TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "locate",
                    "example": "The warehouse is conveniently located near two major interstate highways.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "location",
                    "example": "Our pharmacy chain plans to open five new locations next spring.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "local",
                    "example": "We source all of our restaurant's vegetables from local farms.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "locally",
                    "example": "All of our wooden furniture is handcrafted locally by skilled artisans.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The Boutique Hotel is conveniently _____ just two blocks from the central train station.",
                "answer": "located",
                "base_word": "location",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed - bị động)",
                "vi": "Khách sạn Boutique tọa lạc ở một vị trí thuận tiện chỉ cách nhà ga trung tâm hai dãy nhà."
            }
        },
        "overcrowded": {
            "definition_vi": "quá đông đúc, quá tải người, chật kín",
            "examples_vi": [
                "Ngay khi các vị khách bước vào phòng ăn tối, Sue Lin có thể thấy rằng căn phòng sẽ trở nên quá tải.",
                "Để tránh tình trạng quá đông đúc, chúng tôi đã giới hạn số lượng khách mời mà các thành viên có thể đưa theo."
            ],
            "collocations": [
                "overcrowded room",
                "overcrowded train",
                "become overcrowded",
                "prevent overcrowding"
            ],
            "usage": {
                "structures": [
                    "be / become overcrowded (with + N)"
                ],
                "prepositions": ["with"],
                "collocations": [
                    "severely overcrowded",
                    "overcrowded conditions",
                    "relieve overcrowding",
                    "overcrowded schedule"
                ],
                "tip": "Tiền tố 'over-' mang nghĩa 'quá mức' (too much): overcrowded (quá đông), overpriced (quá đắt), overworked (làm việc quá sức)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "overcrowd",
                    "example": "Organizers sold fewer tickets this year so as not to overcrowd the venue.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "overcrowding",
                    "example": "Adding express buses during rush hour has helped alleviate overcrowding.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "overcrowded",
                    "example": "Commuters complained about the overcrowded subway cars every morning.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The airport built a second terminal to relieve _____ in the main departure lounge.",
                "answer": "overcrowding",
                "base_word": "overcrowded",
                "pos_hint": "danh từ (V-ing)",
                "vi": "Sân bay đã xây dựng thêm nhà ga thứ hai để giảm bớt tình trạng quá tải tại phòng chờ khởi hành chính."
            }
        },
        "register": {
            "definition_vi": "sổ đăng ký, danh sách ghi chép (n.); đăng ký, ghi danh (v.)",
            "examples_vi": [
                "Theo sổ đăng ký, đã có hơn 250 người tham dự buổi hội thảo chiều.",
                "Các khách sạn yêu cầu tất cả khách lưu trú phải đăng ký và cung cấp địa chỉ nhà."
            ],
            "collocations": [
                "register for a seminar",
                "registration desk",
                "registration fee",
                "cash register"
            ],
            "usage": {
                "structures": [
                    "register (sb) for + N (đăng ký tham gia khóa học/hội nghị)",
                    "register with + N (đăng ký với tổ chức nào)"
                ],
                "prepositions": ["for", "with", "at"],
                "collocations": [
                    "online registration",
                    "registration form",
                    "advance registration",
                    "hotel register"
                ],
                "tip": "Khi là động từ mang nghĩa 'đăng ký tham gia một sự kiện/khóa học', 'register' luôn đi kèm giới từ 'for' (register for the workshop)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "registrar",
                    "example": "Students must submit their transcripts to the university registrar's office.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "registered",
                    "example": "Only registered participants will be admitted to the afternoon sessions.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Early _____ for the annual marketing symposium ends on Friday, October 15.",
                "answer": "registration",
                "base_word": "register",
                "pos_hint": "danh từ",
                "vi": "Việc đăng ký sớm cho hội nghị chuyên đề tiếp thị thường niên sẽ kết thúc vào thứ Sáu, ngày 15 tháng 10."
            }
        },
        "select": {
            "definition_vi": "lựa chọn, tuyển chọn (v.); có chọn lọc, ưu tú, dành riêng (adj.)",
            "examples_vi": [
                "Người tham gia hội nghị đã chọn buổi hội thảo tiếp thị trong số các chương trình được đưa ra.",
                "Những người chiến thắng là một nhóm ưu tú được tuyển chọn."
            ],
            "collocations": [
                "select from",
                "wide selection",
                "selection process",
                "a select group"
            ],
            "usage": {
                "structures": [
                    "select + A (from B) (as/to be C)",
                    "a wide selection of + N (nhiều mặt hàng để lựa chọn)"
                ],
                "prepositions": ["from", "for", "as"],
                "collocations": [
                    "randomly selected",
                    "carefully select",
                    "selective about",
                    "natural selection"
                ],
                "tip": "Lưu ý: 'select' vừa là động từ vừa là tính từ (a select group of clients = một nhóm khách hàng chọn lọc/VIP); còn 'selective' là tính từ mang nghĩa 'khắt khe, kỹ tính khi chọn lựa'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "selectively",
                    "example": "The venture capital firm invests selectively in clean-energy startups.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Our downtown showroom features an extensive _____ of imported ceramic tiles.",
                "answer": "selection",
                "base_word": "select",
                "pos_hint": "danh từ số ít",
                "vi": "Phòng trưng bày ở trung tâm thành phố của chúng tôi có một bộ sưu tập đa dạng các loại gạch men nhập khẩu."
            }
        },
        "session": {
            "definition_vi": "phiên họp, buổi sinh hoạt/hội thảo, buổi học",
            "examples_vi": [
                "Các phiên hội thảo buổi sáng thường kín chỗ trước, vì vậy hãy đăng ký sớm.",
                "Do sự phổ biến của khóa học này, chúng tôi sẽ tổ chức thành hai buổi."
            ],
            "collocations": [
                "training session",
                "morning session",
                "in session",
                "question-and-answer session"
            ],
            "usage": {
                "structures": [
                    "be in session (đang họp / đang trong kỳ học)",
                    "hold / conduct / attend a session"
                ],
                "prepositions": ["in", "on", "for"],
                "collocations": [
                    "orientation session",
                    "brainstorming session",
                    "plenary session",
                    "breakout session"
                ],
                "tip": "Rất hay ghép với danh từ đứng trước để tạo cụm danh từ chỉ các buổi họp/đào tạo: 'training session, orientation session, Q&A session'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "session",
                    "example": "Each training session lasts approximately ninety minutes.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "sessional",
                    "example": "The college hired several sessional instructors for the spring term.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All new hires must attend two mandatory training _____ before starting work on the factory floor.",
                "answer": "sessions",
                "base_word": "session",
                "pos_hint": "danh từ số nhiều",
                "vi": "Tất cả nhân viên mới phải tham dự hai buổi đào tạo bắt buộc trước khi bắt đầu làm việc tại xưởng sản xuất."
            }
        },
        "take part in": {
            "definition_vi": "tham gia vào (hoạt động, thảo luận, sự kiện)",
            "examples_vi": [
                "Hình thức của phiên họp này rất thoải mái, điều đó giúp mọi người dễ dàng tham gia vào cuộc thảo luận hơn.",
                "Chúng tôi không thể huy động đủ người tham gia cuộc họp, vì vậy chúng tôi đã hủy nó."
            ],
            "collocations": [
                "take part in a discussion",
                "take an active part in",
                "take part in a survey",
                "invited to take part in"
            ],
            "usage": {
                "structures": [
                    "take (an active) part in + N / V-ing (= participate in)"
                ],
                "prepositions": ["in"],
                "collocations": [
                    "take part in negotiations",
                    "take part in a competition",
                    "eager to take part in",
                    "take part in training"
                ],
                "tip": "Bộ ba đồng nghĩa kinh điển trong TOEIC: 'take part in' = 'participate in' = 'engage in' = 'attend' (chú ý 'attend' không có giới từ 'in')."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "participate",
                    "example": "Employees are encouraged to participate in the company's wellness program.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "participant",
                    "example": "Every survey participant will receive a ten-dollar gift voucher.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "participation",
                    "example": "We would like to thank you for your active participation in today's forum.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "participatory",
                    "example": "The new director favors a more participatory style of management.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Over five hundred employees _____ part in the annual charity marathon last weekend.",
                "answer": "took",
                "base_word": "take part in",
                "pos_hint": "động từ chia quá khứ đơn (V2)",
                "vi": "Hơn năm trăm nhân viên đã tham gia giải chạy marathon từ thiện thường niên vào cuối tuần trước."
            }
        }
    },
    6: {
        "access": {
            "definition_vi": "quyền truy cập, lối vào (n.); truy cập, tiếp cận (dữ liệu, địa điểm) (v.)",
            "examples_vi": [
                "Bạn không thể truy cập vào các tệp tin trừ khi bạn biết mật khẩu.",
                "Chúng tôi đã truy cập thông tin trên trang web của công ty."
            ],
            "collocations": [
                "gain access to",
                "have access to",
                "remote access",
                "easily accessible"
            ],
            "usage": {
                "structures": [
                    "have / gain / grant access to + N (danh từ 'access' luôn đi với giới từ 'to')",
                    "access + N (động từ 'access' cộng trực tiếp tân ngữ, KHÔNG có giới từ 'to')"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "Internet access",
                    "restricted access",
                    "wheelchair accessible",
                    "unauthorized access"
                ],
                "tip": "Bẫy kinh điển trong TOEIC: khi là danh từ thì bắt buộc có 'to' (have/gain access TO the building), nhưng khi là động từ thì KHÔNG có 'to' (access the files)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "accessibility",
                    "example": "The website redesign improved accessibility for visually impaired users.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "accessibly",
                    "example": "The user manual is written accessibly so that beginners can follow it.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new community library is fully _____ to patrons with physical disabilities.",
                "answer": "accessible",
                "base_word": "access",
                "pos_hint": "tính từ",
                "vi": "Thư viện cộng đồng mới hoàn toàn dễ tiếp cận đối với những độc giả khuyết tật về thể chất."
            }
        },
        "allocate": {
            "definition_vi": "phân bổ, cấp phát (ngân sách, thời gian, tài nguyên cho một mục đích cụ thể)",
            "examples_vi": [
                "Quản lý văn phòng đã không phân bổ đủ tiền để mua phần mềm.",
                "Kiến trúc sư phần mềm đã không cấp phát đủ bộ nhớ để card âm thanh hoạt động trên máy tính của bạn."
            ],
            "collocations": [
                "allocate funds",
                "allocate resources",
                "allocate time",
                "budget allocation"
            ],
            "usage": {
                "structures": [
                    "allocate + sth + to / for + N (phân bổ cái gì cho ai/việc gì)",
                    "allocate + sth + to V (phân bổ cái gì để làm gì)"
                ],
                "prepositions": ["to", "for", "among"],
                "collocations": [
                    "resource allocation",
                    "allocate a portion of",
                    "allocated budget",
                    "fairly allocate"
                ],
                "tip": "Thường đi kèm các tân ngữ chỉ tiền bạc, thời gian hoặc nguồn lực (funds, money, budget, time, space, resources) và giới từ 'to/for'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "allocable",
                    "example": "Only travel expenses directly allocable to the client project will be reimbursed.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The city council approved the _____ of two million dollars for road repairs.",
                "answer": "allocation",
                "base_word": "allocate",
                "pos_hint": "danh từ",
                "vi": "Hội đồng thành phố đã phê duyệt việc phân bổ hai triệu đô la để sửa chữa đường sá."
            }
        },
        "compatible": {
            "definition_vi": "tương thích, có thể hoạt động cùng nhau; hòa hợp",
            "examples_vi": [
                "Hệ điều hành này không tương thích với mẫu máy tính này.",
                "Người dùng các ứng dụng phần mềm luôn muốn phiên bản mới tương thích với phiên bản hiện tại."
            ],
            "collocations": [
                "be compatible with",
                "fully compatible",
                "backward compatible",
                "software compatibility"
            ],
            "usage": {
                "structures": [
                    "be compatible with + N (tương thích với thiết bị/hệ thống nào)"
                ],
                "prepositions": ["with"],
                "collocations": [
                    "compatible devices",
                    "check compatibility",
                    "compatible operating system",
                    "mutually compatible"
                ],
                "tip": "Trong TOEIC Part 5, thấy chỗ trống đứng trước giới từ 'with' trong ngữ cảnh máy tính/phần mềm thì 99% đáp án là 'compatible'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "compatibility",
                    "example": "Please verify hardware compatibility before installing the new graphics card.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "compatible",
                    "example": "The wireless printer is compatible with both Windows and Mac computers.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "compatibly",
                    "example": "The two software modules were designed to work compatibly with each other.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Before purchasing the adapter, check its _____ with your laptop model.",
                "answer": "compatibility",
                "base_word": "compatible",
                "pos_hint": "danh từ",
                "vi": "Trước khi mua bộ chuyển đổi, hãy kiểm tra tính tương thích của nó với mẫu máy tính xách tay của bạn."
            }
        },
        "delete": {
            "definition_vi": "xóa bỏ, gạch bỏ (dữ liệu, tệp tin, văn bản)",
            "examples_vi": [
                "Các kỹ thuật viên đã vô tình xóa toàn bộ dữ liệu trên ổ đĩa.",
                "Nút này trên bàn phím dùng để xóa các ký tự khỏi màn hình."
            ],
            "collocations": [
                "delete a file",
                "accidentally delete",
                "delete from the database",
                "deletion of data"
            ],
            "usage": {
                "structures": [
                    "delete + A (from B) (xóa A khỏi B)"
                ],
                "prepositions": ["from"],
                "collocations": [
                    "permanently delete",
                    "delete key",
                    "delete an entry",
                    "recover deleted files"
                ],
                "tip": "Thường đi với giới từ 'from' (delete old records from the system) hoặc dùng ở dạng quá khứ phân từ 'deleted files' (các tệp đã bị xóa)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "delete",
                    "example": "Please delete any duplicate contacts from the customer mailing list.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "deletion",
                    "example": "The editor recommended the deletion of the last two paragraphs.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "deleted",
                    "example": "Our IT specialist was able to recover the accidentally deleted spreadsheet.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Regular cloud backups protect the company against the accidental _____ of critical files.",
                "answer": "deletion",
                "base_word": "delete",
                "pos_hint": "danh từ",
                "vi": "Việc sao lưu đám mây thường xuyên bảo vệ công ty khỏi sự cố vô tình xóa mất các tệp tin quan trọng."
            }
        },
        "display": {
            "definition_vi": "màn hình hiển thị, sự trưng bày (n.); hiển thị, trưng bày, thể hiện (v.)",
            "examples_vi": [
                "Ánh sáng trên màn hình tinh thể lỏng (LCD) quá yếu.",
                "Chương trình kế toán sẽ hiển thị số dư hiện tại khi được mở lên."
            ],
            "collocations": [
                "on display",
                "window display",
                "digital display",
                "display a permit"
            ],
            "usage": {
                "structures": [
                    "be on display (đang được trưng bày)",
                    "clearly display + N (hiển thị rõ ràng cái gì - như thẻ đỗ xe, bảng giá)"
                ],
                "prepositions": ["on", "in", "at"],
                "collocations": [
                    "fireworks display",
                    "display case",
                    "prominently display",
                    "LCD display"
                ],
                "tip": "Cụm giới từ cố định 'on display' (= being exhibited: đang được trưng bày) xuất hiện rất thường xuyên trong cả Part 1, Part 5 và Part 7."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "display",
                    "example": "All visitors must display their security badges at all times.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "display",
                    "example": "New fall merchandise is now on display in the store's front windows.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "displayed",
                    "example": "The displayed prices do not include local sales tax or shipping.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Vehicles parked in the company lot must clearly _____ a valid parking permit on the dashboard.",
                "answer": "display",
                "base_word": "display",
                "pos_hint": "động từ nguyên mẫu (sau động từ khuyết thiếu 'must')",
                "vi": "Các phương tiện đỗ trong bãi xe của công ty phải đặt hiển thị rõ ràng giấy phép đỗ xe hợp lệ trên bảng điều khiển."
            }
        },
        "duplicate": {
            "definition_vi": "sao chép, nhân bản; lặp lại y hệt (thành công) (v.); bản sao (n.); giống hệt (adj.)",
            "examples_vi": [
                "Tôi nghĩ chương trình xử lý văn bản mới sẽ lặp lại được thành công của chương trình đã ra mắt năm ngoái.",
                "Trước khi bạn về, vui lòng nhân bản tệp tin đó bằng cách tạo một bản sao trên đĩa CD-ROM."
            ],
            "collocations": [
                "duplicate a file",
                "in duplicate",
                "duplicate key",
                "avoid duplication"
            ],
            "usage": {
                "structures": [
                    "duplicate + N (sao chép tài liệu / lặp lại thành tích)",
                    "in duplicate (thành hai bản giống nhau)"
                ],
                "prepositions": ["in", "of"],
                "collocations": [
                    "duplicate copy",
                    "duplication of effort",
                    "duplicate receipt",
                    "exact duplicate"
                ],
                "tip": "Từ 'duplicate' có thể làm động từ, danh từ lẫn tính từ mà không đổi cách viết; còn 'duplication' là danh từ chỉ hành động sao chép/sự trùng lặp."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "duplicate",
                    "example": "Please request a duplicate receipt if you need to claim travel expenses.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Merging the two databases will eliminate the unnecessary _____ of customer records.",
                "answer": "duplication",
                "base_word": "duplicate",
                "pos_hint": "danh từ chỉ sự việc",
                "vi": "Việc hợp nhất hai cơ sở dữ liệu sẽ loại bỏ tình trạng trùng lặp không cần thiết của hồ sơ khách hàng."
            }
        },
        "failure": {
            "definition_vi": "sự thất bại; sự hỏng hóc, ngừng hoạt động (máy móc, hệ thống); việc không làm gì đó",
            "examples_vi": [
                "Việc bạn không thông báo cho chúng tôi về mật khẩu đã thay đổi khiến công ty mất một ngày làm việc.",
                "Sự cố hỏng hóc lặp đi lặp lại của chiếc máy in đã làm người kỹ thuật viên bối rối."
            ],
            "collocations": [
                "power failure",
                "mechanical failure",
                "failure to do sth",
                "equipment failure"
            ],
            "usage": {
                "structures": [
                    "failure to + V (việc không làm điều gì theo quy định)",
                    "power / system / engine / crop failure (sự cố mất điện / hỏng hệ thống / mất mùa)"
                ],
                "prepositions": ["to", "of", "in"],
                "collocations": [
                    "fail to comply",
                    "unfailing support",
                    "heart failure",
                    "end in failure"
                ],
                "tip": "Trong văn bản thông báo và hợp đồng TOEIC, cấu trúc 'Failure to + V will result in...' (Việc không làm... sẽ dẫn đến...) xuất hiện cực kỳ nhiều."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "unfailing",
                    "example": "We thank our customers for their unfailing loyalty over the past thirty years.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "unfailingly",
                    "example": "The front desk staff remained unfailingly polite even during peak check-in hours.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The factory had to halt production for three hours yesterday due to a sudden power _____.",
                "answer": "failure",
                "base_word": "failure",
                "pos_hint": "danh từ số ít",
                "vi": "Nhà máy đã phải ngừng sản xuất trong ba giờ ngày hôm qua do sự cố mất điện đột ngột."
            }
        },
        "figure out": {
            "definition_vi": "tìm ra cách giải quyết, hiểu ra, tính toán ra",
            "examples_vi": [
                "Bằng cách kiểm tra tất cả các lỗi, các kỹ thuật viên đã tìm ra cách khắc phục sự cố.",
                "Chúng tôi tính ra rằng sẽ mất ít nhất mười phút để tải tệp tin đó xuống."
            ],
            "collocations": [
                "figure out how to",
                "figure out a problem",
                "figure out the cause",
                "figure out a way"
            ],
            "usage": {
                "structures": [
                    "figure out + N / figure + N + out",
                    "figure out + how/what/why + to V / mệnh đề"
                ],
                "prepositions": ["out"],
                "collocations": [
                    "try to figure out",
                    "hard to figure out",
                    "sales figures",
                    "key figure"
                ],
                "tip": "Bản thân từ 'figure' khi đứng độc lập còn là danh từ rất phổ biến trong TOEIC mang nghĩa 'con số thống kê' (sales figures) hoặc 'nhân vật' (a public figure)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "figure",
                    "example": "Shipping costs figure prominently in our decision to choose a local supplier.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "figure",
                    "example": "According to the latest sales figures, our revenue grew by eight percent.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "figurative",
                    "example": "The speaker used figurative language to describe the company's journey.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "figuratively",
                    "example": "The new product launch put our small startup on the map, figuratively speaking.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "It took the IT department several hours to _____ out why the server kept crashing.",
                "answer": "figure",
                "base_word": "figure out",
                "pos_hint": "động từ nguyên mẫu (sau 'to')",
                "vi": "Bộ phận công nghệ thông tin đã mất vài giờ để tìm ra lý do tại sao máy chủ liên tục bị sập."
            }
        },
        "ignore": {
            "definition_vi": "phớt lờ, bỏ qua, không chú ý đến",
            "examples_vi": [
                "Khi bà giám đốc đang làm việc bên máy tính, bà không để ý đến bất cứ thứ gì xung quanh mình.",
                "Đừng phớt lờ lời khuyên của kỹ thuật viên khi kết nối dây cáp."
            ],
            "collocations": [
                "ignore a warning",
                "ignore advice",
                "completely ignore",
                "cannot be ignored"
            ],
            "usage": {
                "structures": [
                    "ignore + N (warning / advice / complaint / rule)",
                    "be ignorant of + N (không biết về điều gì)"
                ],
                "prepositions": ["of", "by"],
                "collocations": [
                    "ignore a request",
                    "willfully ignore",
                    "ignorance of the law",
                    "blissfully ignorant"
                ],
                "tip": "Chú ý: động từ 'ignore' là 'cố tình phớt lờ', còn tính từ 'ignorant (of)' và danh từ 'ignorance (of)' mang nghĩa 'thiếu hiểu biết/không biết về điều gì'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "ignorant",
                    "example": "Many consumers remain ignorant of the new data privacy regulations.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "ignorantly",
                    "example": "He ignorantly signed the contract without reading the fine print.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Please _____ the previous billing statement if you have already submitted your payment.",
                "answer": "ignore",
                "base_word": "ignore",
                "pos_hint": "động từ nguyên mẫu (câu mệnh lệnh)",
                "vi": "Vui lòng bỏ qua bảng sao kê thanh toán trước đó nếu bạn đã gửi khoản thanh toán của mình."
            }
        },
        "search": {
            "definition_vi": "cuộc tìm kiếm, sự tra cứu (n.); tìm kiếm, rà soát (v.)",
            "examples_vi": [
                "Việc tra cứu cơ sở dữ liệu của chúng tôi mang lại rất ít thông tin.",
                "Máy tính đã tìm kiếm tất cả những cái tên bắt đầu bằng chữ W."
            ],
            "collocations": [
                "search for",
                "in search of",
                "job search",
                "search engine"
            ],
            "usage": {
                "structures": [
                    "search (A) for B (lục tìm khắp nơi A để tìm kiếm mục tiêu B)",
                    "in search of + N (để tìm kiếm cái gì)"
                ],
                "prepositions": ["for", "of", "through"],
                "collocations": [
                    "thorough search",
                    "conduct a search",
                    "search the database",
                    "searchable archive"
                ],
                "tip": "Phân biệt: 'search the database' (tìm trong cơ sở dữ liệu - nơi tìm kiếm) và 'search FOR the file' (tìm kiếm tệp tin - thứ cần tìm)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "search",
                    "example": "The committee is still searching for a suitable candidate to fill the vacancy.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "search",
                    "example": "A thorough search of the warehouse failed to locate the missing crate.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "searchable",
                    "example": "All past issues of the newsletter are now available in a searchable online archive.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "searchingly",
                    "example": "The auditor questioned the chief accountant searchingly about the discrepancy.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The library has digitized its historical newspapers into a fully _____ online database.",
                "answer": "searchable",
                "base_word": "search",
                "pos_hint": "tính từ",
                "vi": "Thư viện đã số hóa các tờ báo lịch sử của mình thành một cơ sở dữ liệu trực tuyến có thể tra cứu toàn diện."
            }
        },
        "shut down": {
            "definition_vi": "tắt máy (máy tính, thiết bị); đóng cửa, ngừng hoạt động (nhà máy, công ty)",
            "examples_vi": [
                "Vui lòng tắt máy tính trước khi bạn rời đi.",
                "Chúng tôi luôn tắt hệ thống điều hòa không khí vào dịp cuối tuần."
            ],
            "collocations": [
                "shut down a computer",
                "shut down a factory",
                "system shutdown",
                "temporary shutdown"
            ],
            "usage": {
                "structures": [
                    "shut down + N / shut + N + down (tắt máy / đóng cửa nhà máy)",
                    "shut down (nội động từ: ngừng hoạt động)"
                ],
                "prepositions": ["down"],
                "collocations": [
                    "emergency shutdown",
                    "plant shutdown",
                    "completely shut down",
                    "automatically shut down"
                ],
                "tip": "Chú ý: viết tách 2 chữ 'shut down' là cụm động từ (phrasal verb), còn viết liền 1 chữ 'shutdown' là danh từ (a temporary plant shutdown)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "shut",
                    "example": "Please make sure all windows are tightly shut before leaving the office.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "shutdown",
                    "example": "The annual maintenance shutdown of the assembly plant is scheduled for August.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "shut",
                    "example": "The fire doors must be kept shut at all times to comply with safety codes.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The manufacturing plant will undergo a two-week _____ in July for equipment upgrades.",
                "answer": "shutdown",
                "base_word": "shut down",
                "pos_hint": "danh từ số ít (viết liền)",
                "vi": "Nhà máy sản xuất sẽ trải qua một đợt ngừng hoạt động kéo dài hai tuần vào tháng Bảy để nâng cấp thiết bị."
            }
        },
        "warning": {
            "definition_vi": "lời cảnh báo, dấu hiệu báo trước nguy hiểm/sự cố",
            "examples_vi": [
                "Đèn nhấp nháy màu đỏ đưa ra cảnh báo cho người dùng rằng pin đang yếu.",
                "Những hình ảnh nhấp nháy trên trang web là các cảnh báo nhằm thu hút sự chú ý của người dùng."
            ],
            "collocations": [
                "without warning",
                "issue a warning",
                "warning sign",
                "advance warning"
            ],
            "usage": {
                "structures": [
                    "give / issue a warning (to sb) (about/against sth)",
                    "warn + sb + to V / not to V / that + mệnh đề"
                ],
                "prepositions": ["about", "against", "of", "without"],
                "collocations": [
                    "early warning system",
                    "written warning",
                    "weather warning",
                    "heed a warning"
                ],
                "tip": "Cụm giới từ cố định 'without warning' (= suddenly/unexpectedly: không báo trước, đột ngột) rất hay gặp trong bài đọc TOEIC."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "warningly",
                    "example": "The supervisor looked warningly at the staff members who arrived late.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Meteorologists have _____ residents that heavy snowstorms could disrupt commuter rail service.",
                "answer": "warned",
                "base_word": "warning",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed)",
                "vi": "Các nhà khí tượng học đã cảnh báo người dân rằng bão tuyết lớn có thể làm gián đoạn dịch vụ tàu điện ngoại ô."
            }
        }
    },
    7: {
        "affordable": {
            "definition_vi": "có giá cả phải chăng, vừa túi tiền, có khả năng chi trả",
            "examples_vi": [
                "Ưu tiên hàng đầu của công ty là tìm kiếm một hệ thống điện thoại có giá cả phải chăng.",
                "Rõ ràng là những hệ thống máy tính vừa tầm chi trả đối với một công ty trong nhóm Fortune 500 sẽ không hề vừa túi tiền đối với một công ty nhỏ."
            ],
            "collocations": [
                "affordable prices",
                "affordable housing",
                "easily affordable",
                "can afford to"
            ],
            "usage": {
                "structures": [
                    "affordable + N (prices / rates / housing / healthcare)",
                    "can / be able to afford + N / to V (đủ khả năng chi trả cho)"
                ],
                "prepositions": ["for", "to"],
                "collocations": [
                    "at an affordable rate",
                    "make sth affordable",
                    "affordable alternative",
                    "reasonably affordable"
                ],
                "tip": "Tính từ 'affordable' luôn mang nghĩa tích cực (= reasonably priced / inexpensive) và cực kỳ hay xuất hiện trong các bài quảng cáo sản phẩm/dịch vụ."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "affordably",
                    "example": "The new furniture line is both stylishly designed and affordably priced.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Small startups often cannot _____ to hire a full-time legal team.",
                "answer": "afford",
                "base_word": "affordable",
                "pos_hint": "động từ nguyên mẫu (sau 'cannot')",
                "vi": "Các công ty khởi nghiệp nhỏ thường không đủ khả năng tài chính để thuê một đội ngũ pháp lý toàn thời gian."
            }
        },
        "as needed": {
            "definition_vi": "khi cần thiết, tùy theo nhu cầu thực tế",
            "examples_vi": [
                "Dịch vụ chuyển phát nhanh không đến mỗi ngày, mà chỉ đến khi cần thiết.",
                "Hợp đồng dịch vụ nêu rõ rằng việc sửa chữa sẽ được thực hiện trên cơ sở khi nào cần thì làm."
            ],
            "collocations": [
                "on an as-needed basis",
                "order supplies as needed",
                "adjust as needed",
                "hire staff as needed"
            ],
            "usage": {
                "structures": [
                    "V + as needed (= as necessary: khi cần thiết)",
                    "on an as-needed basis (trên cơ sở khi nào cần thì cung cấp/thực hiện)"
                ],
                "prepositions": ["as", "on"],
                "collocations": [
                    "replenish stock as needed",
                    "update records as needed",
                    "work overtime as needed",
                    "schedule maintenance as needed"
                ],
                "tip": "Ghi nhớ cụm cố định 'on an as-needed basis' (tùy theo nhu cầu phát sinh) và lưu ý 'as needed' là rút gọn của mệnh đề 'as it is needed'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "need",
                    "example": "Please let the receptionist know if you need any assistance with your luggage.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "need",
                    "example": "There is a growing need for bilingual customer service representatives.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "needed",
                    "example": "The government grant provided much-needed funding for the research lab.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "needfully",
                    "example": "All safety equipment was needfully inspected prior to the plant reopening.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Temporary warehouse workers are hired on an as-_____ basis during the holiday shopping season.",
                "answer": "needed",
                "base_word": "as needed",
                "pos_hint": "quá khứ phân từ / tính từ (trong cụm cố định)",
                "vi": "Nhân viên kho thời vụ được thuê trên cơ sở khi nào cần thì tuyển trong suốt mùa mua sắm lễ hội."
            }
        },
        "be in charge of": {
            "definition_vi": "phụ trách, chịu trách nhiệm quản lý/điều hành (ai/việc gì)",
            "examples_vi": [
                "Ông ấy đã bổ nhiệm một người phụ trách việc duy trì nguồn giấy trong máy fax.",
                "Máy tính của bạn không nên làm chủ bạn, mà đúng hơn là bạn phải làm chủ chiếc máy tính của mình."
            ],
            "collocations": [
                "be in charge of a department",
                "put sb in charge of",
                "take charge of",
                "person in charge"
            ],
            "usage": {
                "structures": [
                    "be in charge of + N / V-ing (= be responsible for)",
                    "take charge of + N (tiếp quản, đứng ra phụ trách)",
                    "put sb in charge of + N (giao cho ai phụ trách)"
                ],
                "prepositions": ["in", "of"],
                "collocations": [
                    "officer in charge",
                    "left in charge of",
                    "in charge of hiring",
                    "in charge of operations"
                ],
                "tip": "Cụm 'be in charge of + N/V-ing' đồng nghĩa trực tiếp với 'be responsible for' và 'oversee / supervise' trong các câu hỏi đọc hiểu TOEIC."
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
                    "example": "Delivery is free of charge for all orders exceeding fifty dollars.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "chargeable",
                    "example": "Any repairs caused by user negligence are chargeable to the customer.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Ms. Gomez has been placed in _____ of coordinating the international marketing campaign.",
                "answer": "charge",
                "base_word": "be in charge of",
                "pos_hint": "danh từ (trong cụm 'in charge of')",
                "vi": "Cô Gomez đã được giao phụ trách việc điều phối chiến dịch tiếp thị quốc tế."
            }
        },
        "capacity": {
            "definition_vi": "sức chứa, công suất tối đa, dung lượng; năng lực; tư cách/chức vụ",
            "examples_vi": [
                "Phòng hội nghị mới rộng hơn nhiều và có sức chứa một trăm người.",
                "Yêu cầu bộ nhớ của ứng dụng phần mềm này vượt quá dung lượng máy tính của chúng ta."
            ],
            "collocations": [
                "seating capacity",
                "at full capacity",
                "storage capacity",
                "in the capacity of"
            ],
            "usage": {
                "structures": [
                    "have a capacity of + con số (có sức chứa là...)",
                    "operate / run at (full) capacity (hoạt động hết công suất)",
                    "in one's capacity as + chức danh (với tư cách là...)"
                ],
                "prepositions": ["of", "at", "in", "for"],
                "collocations": [
                    "production capacity",
                    "exceed the capacity",
                    "expand capacity",
                    "maximum capacity"
                ],
                "tip": "Học thuộc lòng 2 cụm giới từ cực hay gặp: 'at full capacity' (hết công suất/kín chỗ) và 'in his/her capacity as...' (với tư cách/cương vị là...)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "capacitate",
                    "example": "Specialized training programs capacitate employees to handle complex machinery.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "capacity",
                    "example": "The stadium has a seating capacity of over fifty thousand spectators.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "capacious",
                    "example": "The new SUV features a capacious trunk suitable for family road trips.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "capaciously",
                    "example": "The exhibition hall was capaciously designed to host multiple trade shows.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To meet holiday demand, our manufacturing plants are currently operating at full _____.",
                "answer": "capacity",
                "base_word": "capacity",
                "pos_hint": "danh từ",
                "vi": "Để đáp ứng nhu cầu dịp lễ, các nhà máy sản xuất của chúng tôi hiện đang hoạt động hết công suất."
            }
        },
        "durable": {
            "definition_vi": "bền, chắc chắn, sử dụng được lâu dài",
            "examples_vi": [
                "Chiếc máy in này bền đến mức chỉ cần giữ gìn một chút là nó sẽ dùng được thêm năm năm nữa.",
                "Những chiếc ghế này bền hơn những chiếc đầu tiên mà chúng ta đã xem."
            ],
            "collocations": [
                "durable goods",
                "durable material",
                "lightweight and durable",
                "proven durability"
            ],
            "usage": {
                "structures": [
                    "be durable enough to V",
                    "durable + N (goods / fabric / plastic / construction)"
                ],
                "prepositions": ["for", "under"],
                "collocations": [
                    "highly durable",
                    "durable finish",
                    "test for durability",
                    "long-lasting durability"
                ],
                "tip": "Từ khóa quen thuộc khi mô tả ưu điểm của thiết bị văn phòng, nội thất, hành lý hoặc quần áo bảo hộ trong TOEIC."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "durability",
                    "example": "Our outdoor furniture is famous for its exceptional durability in harsh weather.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "durable",
                    "example": "The hiking boots are made from waterproof and durable leather.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "durably",
                    "example": "These industrial laptops are durably built to withstand drops and vibrations.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All of our luggage undergoes rigorous testing to ensure maximum _____ during air travel.",
                "answer": "durability",
                "base_word": "durable",
                "pos_hint": "danh từ",
                "vi": "Tất cả hành lý của chúng tôi đều trải qua quá trình kiểm tra nghiêm ngặt để đảm bảo độ bền tối đa trong các chuyến bay."
            }
        },
        "initiative": {
            "definition_vi": "sáng kiến, chương trình hành động mới; sự chủ động, tính tiên phong",
            "examples_vi": [
                "Nhân viên được khuyến khích phát huy tính chủ động và chia sẻ ý tưởng của họ với ban quản lý.",
                "Sáng kiến công nghệ của chúng tôi bao gồm một hệ thống cơ sở dữ liệu mới đầy thú vị và sẽ giúp chúng tôi cách mạng hóa dịch vụ khách hàng."
            ],
            "collocations": [
                "take the initiative",
                "new initiative",
                "launch an initiative",
                "on one's own initiative"
            ],
            "usage": {
                "structures": [
                    "take the initiative (to V) (đi bước đầu tiên / chủ động làm gì - không đếm được)",
                    "launch / support an initiative (phát động một chương trình/sáng kiến mới - đếm được)"
                ],
                "prepositions": ["on", "to", "for"],
                "collocations": [
                    "cost-cutting initiative",
                    "green initiative",
                    "government initiative",
                    "show initiative"
                ],
                "tip": "Mẹo phân biệt 2 danh từ của động từ 'initiate': 'initiative' là 'sáng kiến/sự chủ động', còn 'initiation' là 'sự bắt đầu/lễ kết nạp'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "initial",
                    "example": "The initial response to our advertising campaign has been overwhelmingly positive.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "initially",
                    "example": "The bridge project was initially scheduled for completion in May.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The mayor announced a new _____ aimed at revitalizing small businesses in the downtown area.",
                "answer": "initiative",
                "base_word": "initiative",
                "pos_hint": "danh từ số ít (sáng kiến/chương trình)",
                "vi": "Thị trưởng đã công bố một sáng kiến mới nhằm hồi sinh các doanh nghiệp nhỏ ở khu vực trung tâm thành phố."
            }
        },
        "physically": {
            "definition_vi": "về mặt thể chất, thuộc về cơ thể; một cách trực tiếp/vật lý",
            "examples_vi": [
                "Màn hình máy tính đang làm cô ấy cảm thấy mệt mỏi về mặt thể chất.",
                "Việc trực tiếp di chuyển màn hình của bạn từ vị trí này sang vị trí khác trên bàn làm việc có thể giúp giảm hội chứng căng cơ do giữ nguyên một tư thế."
            ],
            "collocations": [
                "physically demanding",
                "physically present",
                "physically fit",
                "physically impossible"
            ],
            "usage": {
                "structures": [
                    "physically + Adj / V3-ed (physically demanding / exhausting / located)",
                    "physically + V (trực tiếp làm gì bằng tay chân/cơ thể)"
                ],
                "prepositions": ["in", "at"],
                "collocations": [
                    "physical examination",
                    "physical therapy",
                    "physically active",
                    "physical inventory"
                ],
                "tip": "Cụm 'physically demanding' (đòi hỏi nhiều thể lực) và 'physical examination' (khám sức khỏe tổng quát) rất hay xuất hiện trong TOEIC."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "physician",
                    "example": "Employees absent for more than three days must provide a note from a physician.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Warehouse applicants must be capable of performing _____ demanding tasks such as lifting heavy boxes.",
                "answer": "physically",
                "base_word": "physically",
                "pos_hint": "trạng từ (bổ nghĩa cho tính từ 'demanding')",
                "vi": "Các ứng viên làm việc tại kho phải có khả năng thực hiện các công việc đòi hỏi thể lực như nâng các thùng hàng nặng."
            }
        },
        "provider": {
            "definition_vi": "nhà cung cấp (thường dùng cho dịch vụ như viễn thông, Internet, y tế)",
            "examples_vi": [
                "Bộ phận đã vô cùng hài lòng với dịch vụ mà họ nhận được từ nhà cung cấp điện thoại.",
                "Là nhà cung cấp dịch vụ y tế của bạn, chúng tôi muốn đảm bảo rằng bạn luôn vui vẻ và hài lòng với dịch vụ mình đang nhận được."
            ],
            "collocations": [
                "service provider",
                "Internet service provider",
                "healthcare provider",
                "leading provider"
            ],
            "usage": {
                "structures": [
                    "a provider of + N (nhà cung cấp dịch vụ/sản phẩm gì)",
                    "N + provider (Internet/insurance/utility provider)"
                ],
                "prepositions": ["of", "for"],
                "collocations": [
                    "network provider",
                    "wireless provider",
                    "childcare provider",
                    "primary provider"
                ],
                "tip": "'Provider' thường dùng cho nhà cung cấp dịch vụ (Internet/healthcare/insurance provider), còn 'supplier' thường dùng cho nhà cung cấp hàng hóa/linh kiện."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "provisional",
                    "example": "A provisional budget has been set up for the first quarter of next year.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "provisionally",
                    "example": "The dates for the training workshop have been provisionally approved.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Switching to a new cellular service _____ saved our company nearly $400 a month.",
                "answer": "provider",
                "base_word": "provider",
                "pos_hint": "danh từ số ít",
                "vi": "Việc chuyển sang một nhà cung cấp dịch vụ di động mới đã giúp công ty chúng tôi tiết kiệm gần 400 đô la mỗi tháng."
            }
        },
        "recur": {
            "definition_vi": "tái diễn, lặp lại, xảy ra một lần nữa (thường là lỗi, vấn đề, chi phí)",
            "examples_vi": [
                "Chủ đề doanh số bán hàng sụt giảm cứ lặp đi lặp lại trong mỗi cuộc họp, đôi khi đến vài lần.",
                "Các nhà quản lý không muốn lỗi cụ thể đó tái diễn."
            ],
            "collocations": [
                "recurring problem",
                "recurring fee",
                "prevent from recurring",
                "recurrence of an error"
            ],
            "usage": {
                "structures": [
                    "S + recur (nội động từ - KHÔNG chia bị động)",
                    "prevent + N + from recurring"
                ],
                "prepositions": ["in", "at"],
                "collocations": [
                    "recurring theme",
                    "monthly recurring charge",
                    "frequent recurrence",
                    "recurring issue"
                ],
                "tip": "Chú ý gấp đôi phụ âm 'r' khi thêm đuôi '-ed', '-ing', '-ence': recur -> recurred, recurring, recurrence."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "recurrent",
                    "example": "The software update finally fixed a recurrent bug in the billing module.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "recurrently",
                    "example": "Funding shortages have recurrently delayed the highway expansion project.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Engineers replaced the faulty valve to prevent the leak from _____ in the future.",
                "answer": "recurring",
                "base_word": "recur",
                "pos_hint": "danh động từ (V-ing sau giới từ 'from')",
                "vi": "Các kỹ sư đã thay thế chiếc van bị hỏng để ngăn chặn sự cố rò rỉ tái diễn trong tương lai."
            }
        },
        "reduction": {
            "definition_vi": "sự cắt giảm, sự thu gọn, mức giảm giá",
            "examples_vi": [
                "Cửa hàng đại lý đã giảm giá 20 phần trăm cho các loại kệ và tủ sách.",
                "Việc cắt giảm nhân sự văn phòng đã khiến cho việc tự động hóa thêm nhiều chức năng công việc trở nên cần thiết."
            ],
            "collocations": [
                "cost reduction",
                "price reduction",
                "reduction in staff",
                "significant reduction"
            ],
            "usage": {
                "structures": [
                    "a reduction in + N (sự cắt giảm về số lượng/chi phí/nhân sự)",
                    "a reduction of + số lượng/% (mức giảm bao nhiêu phần trăm)"
                ],
                "prepositions": ["in", "of"],
                "collocations": [
                    "noise reduction",
                    "tax reduction",
                    "waste reduction",
                    "drastic reduction"
                ],
                "tip": "Danh từ 'reduction' cực kỳ hay đi kèm giới từ 'in' để chỉ lĩnh vực/đối tượng được giảm (a reduction in operating costs / a reduction in accidents)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "reduced",
                    "example": "Winter coats are now on sale at significantly reduced prices.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Switching to digital invoicing has led to a substantial _____ in paper and postage expenses.",
                "answer": "reduction",
                "base_word": "reduction",
                "pos_hint": "danh từ số ít",
                "vi": "Việc chuyển sang hóa đơn điện tử đã dẫn đến sự sụt giảm đáng kể chi phí giấy tờ và bưu phí."
            }
        },
        "stay on top of": {
            "definition_vi": "nắm bắt sát sao, cập nhật kịp thời, kiểm soát tốt (tình hình, công việc, xu hướng)",
            "examples_vi": [
                "Để nắm bắt sát sao tiến độ làm việc của nhân viên, bà đã sắp xếp các cuộc họp ăn sáng hàng tuần.",
                "Trong ngành công nghiệp này, bạn phải luôn cập nhật kịp thời những bước phát triển hiện tại."
            ],
            "collocations": [
                "stay on top of things",
                "stay on top of trends",
                "stay on top of deadlines",
                "keep on top of"
            ],
            "usage": {
                "structures": [
                    "stay / keep on top of + N (nắm bắt kịp thời / kiểm soát tốt cái gì)"
                ],
                "prepositions": ["on", "of"],
                "collocations": [
                    "stay on top of current developments",
                    "stay on top of one's workload",
                    "stay on top of market changes",
                    "stay on top of the news"
                ],
                "tip": "Cụm thành ngữ này hoàn toàn đồng nghĩa với 'keep up with' hoặc 'keep track of' (theo kịp / theo dõi sát sao thông tin mới nhất)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "top",
                    "example": "Fourth-quarter earnings topped ten million dollars for the first time.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "top",
                    "example": "Please write your account number at the top of the application form.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "topmost",
                    "example": "Passenger safety is always the topmost priority for our airline.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Subscribing to industry journals helps our engineers stay on _____ of emerging technologies.",
                "answer": "top",
                "base_word": "stay on top of",
                "pos_hint": "danh từ (trong cụm cố định 'stay on top of')",
                "vi": "Việc đặt mua các tạp chí chuyên ngành giúp các kỹ sư của chúng tôi luôn nắm bắt kịp thời những công nghệ mới nổi."
            }
        },
        "stock": {
            "definition_vi": "tích trữ, chất hàng lên kệ, có sẵn trong kho (v.); hàng tồn kho, nguồn cung, cổ phiếu (n.)",
            "examples_vi": [
                "Các nhân viên chất hàng lên kệ theo định kỳ hàng tuần.",
                "Nguồn mực dự trữ cho máy fax của văn phòng đang nhanh chóng cạn kiệt."
            ],
            "collocations": [
                "in stock",
                "out of stock",
                "stock up on",
                "stock market"
            ],
            "usage": {
                "structures": [
                    "be in stock (còn hàng) >< be out of stock (hết hàng)",
                    "stock up on + N (mua tích trữ mặt hàng gì)"
                ],
                "prepositions": ["in", "out", "of", "with", "on"],
                "collocations": [
                    "fully stocked",
                    "stock the shelves",
                    "stockholder",
                    "limited stock"
                ],
                "tip": "Hai cụm giới từ 'in stock' (còn hàng) và 'out of stock' (hết hàng) là từ vựng bắt buộc phải thuộc lòng khi làm bài TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "restock",
                    "example": "Night shift workers restock the supermarket shelves before the store opens.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "stock",
                    "example": "We apologize that the item you ordered is temporarily out of stock.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "stocked",
                    "example": "The employee break room is always well stocked with coffee and snacks.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The supply closet is fully _____ with printer paper, toner cartridges, and envelopes.",
                "answer": "stocked",
                "base_word": "stock",
                "pos_hint": "động từ chia quá khứ phân từ / tính từ (V3/ed)",
                "vi": "Tủ đựng đồ tiếp tế được tích trữ đầy đủ giấy in, hộp mực và phong bì."
            }
        }
    },
    8: {
        "appreciation": {
            "definition_vi": "sự cảm kích, lòng biết ơn; sự đánh giá cao, sự ghi nhận; sự tăng giá trị (tài sản)",
            "examples_vi": [
                "Để ghi nhận sự làm việc chăm chỉ của các bạn trong dự án Castcon, bộ phận sẽ tổ chức một bữa tiệc trưa thân mật vào ngày mùng 3 tháng 11.",
                "Sự trân trọng của bạn đối với những nỗ lực của tôi đã truyền cảm hứng cho tôi vượt qua những giai đoạn cuối cùng của công trình xây dựng."
            ],
            "collocations": [
                "in appreciation of",
                "express appreciation",
                "show appreciation for",
                "deep appreciation"
            ],
            "usage": {
                "structures": [
                    "in appreciation of / for + N (để bày tỏ lòng biết ơn/ghi nhận đối với...)",
                    "appreciate + N / V-ing (trân trọng/cảm kích việc gì - sau appreciate là V-ing)"
                ],
                "prepositions": ["in", "of", "for"],
                "collocations": [
                    "token of appreciation",
                    "certificate of appreciation",
                    "sincere appreciation",
                    "greatly appreciate"
                ],
                "tip": "Cụm giới từ mở đầu câu 'In appreciation of your hard work / loyalty...' (Để tri ân sự cống hiến/gắn bó của bạn...) xuất hiện rất nhiều trong thư từ nội bộ TOEIC."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "appreciative",
                    "example": "The charity organization was deeply appreciative of our company's generous donation.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "appreciatively",
                    "example": "The audience nodded appreciatively as the director thanked the technical crew.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "We would greatly _____ it if you could return the signed contract by the end of the week.",
                "answer": "appreciate",
                "base_word": "appreciation",
                "pos_hint": "động từ nguyên mẫu (sau 'would')",
                "vi": "Chúng tôi sẽ vô cùng cảm kích nếu bạn có thể gửi lại bản hợp đồng đã ký trước cuối tuần này."
            }
        },
        "be made of": {
            "definition_vi": "được làm bằng (chất liệu gì); có phẩm chất/bản lĩnh gì",
            "examples_vi": [
                "Công việc này sẽ thực sự thử thách xem bản lĩnh của bạn đến đâu.",
                "Mọi người nói rằng nhà đàm phán đó có tinh thần thép."
            ],
            "collocations": [
                "be made of wood",
                "be made of recycled materials",
                "see what sb is made of",
                "nerves made of steel"
            ],
            "usage": {
                "structures": [
                    "be made of + chất liệu (giữ nguyên bản chất vật lý như gỗ, kim loại, nhựa)",
                    "what + sb + be made of (bản lĩnh/phẩm chất tiềm ẩn của ai)"
                ],
                "prepositions": ["of", "from", "by"],
                "collocations": [
                    "be made of stainless steel",
                    "be made of solid oak",
                    "be made of durable plastic",
                    "custom-made"
                ],
                "tip": "'Be made of' chỉ chất liệu nhìn thấy rõ (made of wood/glass), 'be made from' chỉ nguyên liệu đã biến đổi (paper is made from trees), nhưng trong nghĩa bóng 'see what you are made of' có nghĩa là 'xem bản lĩnh/năng lực của bạn thế nào'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "make",
                    "example": "The factory makes precision components for the aerospace industry.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "maker",
                    "example": "The automaker announced plans to launch three electric vehicles next year.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "making",
                    "example": "This documentary was three years in the making.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "made",
                    "example": "All of our chocolates are freshly made on the premises every morning.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "All of our eco-friendly packaging boxes are _____ of 100 percent post-consumer recycled cardboard.",
                "answer": "made",
                "base_word": "be made of",
                "pos_hint": "quá khứ phân từ (V3/ed)",
                "vi": "Tất cả các hộp bao bì thân thiện với môi trường của chúng tôi đều được làm từ 100% bìa cứng tái chế sau tiêu dùng."
            }
        },
        "bring in": {
            "definition_vi": "tuyển dụng, mời thêm (chuyên gia, nhân sự từ bên ngoài vào); mang lại (doanh thu, lợi nhuận)",
            "examples_vi": [
                "Chủ tịch công ty muốn mời thêm một chuyên gia tư vấn hiệu suất làm việc.",
                "Công ty đã đưa vào một đội ngũ lập kế hoạch dự án mới."
            ],
            "collocations": [
                "bring in a consultant",
                "bring in new clients",
                "bring in revenue",
                "bring in experts"
            ],
            "usage": {
                "structures": [
                    "bring in + sb (hire / recruit an outside specialist)",
                    "bring in + tiền/doanh thu (generate revenue / profits)"
                ],
                "prepositions": ["in", "on"],
                "collocations": [
                    "bring in outside help",
                    "bring in new business",
                    "bring in a verdict",
                    "bring in new regulations"
                ],
                "tip": "Trong TOEIC, 'bring in' có 2 nghĩa rất hay gặp: (1) thuê chuyên gia/nhân sự bên ngoài vào hỗ trợ, và (2) mang về doanh thu hoặc khách hàng mới."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "bring",
                    "example": "Please remember to bring your identification card to the training session.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "brought",
                    "example": "The expertise brought by our new director has revitalized the sales team.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To resolve the complex tax audit, the board _____ in an independent accounting firm last month.",
                "answer": "brought",
                "base_word": "bring in",
                "pos_hint": "động từ chia quá khứ đơn (V2)",
                "vi": "Để giải quyết cuộc kiểm toán thuế phức tạp, hội đồng quản trị đã mời vào một công ty kế toán độc lập hồi tháng trước."
            }
        },
        "casually": {
            "definition_vi": "một cách thoải mái, thân mật, không trang trọng (trang phục, lời nói); tình cờ",
            "examples_vi": [
                "Vào các ngày thứ Sáu, hầu hết nhân viên đều ăn mặc thoải mái.",
                "Martin nói chuyện một cách tự nhiên thoải mái như thể anh đang tán gẫu với bạn bè."
            ],
            "collocations": [
                "dress casually",
                "mention casually",
                "speak casually",
                "casual attire"
            ],
            "usage": {
                "structures": [
                    "dress + casually (ăn mặc giản dị/thoải mái)",
                    "casual + N (attire / wear / Friday / dining)"
                ],
                "prepositions": ["in"],
                "collocations": [
                    "business casual",
                    "casual conversation",
                    "casual observer",
                    "casually dressed"
                ],
                "tip": "Gắn liền với văn hóa công sở trong TOEIC: 'dress casually' (mặc đồ tự do thoải mái) và 'business casual' (trang phục công sở lịch sự nhưng không cần comple/cà vạt)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "casualness",
                    "example": "Despite the casualness of the lunch meeting, several key decisions were made.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "casual",
                    "example": "Employees are permitted to wear casual attire on Fridays during the summer.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "casually",
                    "example": "She casually remarked that she might apply for the branch manager position.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Although the company picnic is a _____ event, employees are still expected to behave professionally.",
                "answer": "casual",
                "base_word": "casually",
                "pos_hint": "tính từ (bổ nghĩa cho danh từ 'event')",
                "vi": "Mặc dù buổi dã ngoại của công ty là một sự kiện thân mật thoải mái, nhân viên vẫn được kỳ vọng sẽ cư xử chuyên nghiệp."
            }
        },
        "code": {
            "definition_vi": "quy tắc ứng xử, bộ luật; mã số, mật mã (n.); mã hóa, lập trình (v.)",
            "examples_vi": [
                "Các nhân viên mới đã quan sát quy tắc ứng xử bất thành văn trong tuần đầu tiên làm việc.",
                "Ngay cả những công ty truyền thống nhất cũng đang thay đổi quy định về trang phục của họ theo hướng bớt trang trọng hơn."
            ],
            "collocations": [
                "dress code",
                "code of conduct",
                "postal code",
                "building code"
            ],
            "usage": {
                "structures": [
                    "code of conduct / ethics (quy tắc ứng xử / đạo đức nghề nghiệp)",
                    "dress / safety / building / fire code (quy định về trang phục / an toàn / xây dựng / phòng cháy)"
                ],
                "prepositions": ["of", "in"],
                "collocations": [
                    "zip code",
                    "area code",
                    "promotional code",
                    "color-coded files"
                ],
                "tip": "Hai cụm danh từ 'dress code' (quy định trang phục) và 'code of conduct' (quy tắc ứng xử) xuất hiện cực nhiều trong sổ tay nhân viên (employee handbook) ở Part 7."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "coder",
                    "example": "The hospital hired two medical coders to process insurance claims.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Filing cabinets in the medical clinic use _____ labels so staff can locate patient charts quickly.",
                "answer": "coded",
                "base_word": "code",
                "pos_hint": "tính từ (V3/ed)",
                "vi": "Các tủ hồ sơ tại phòng khám y tế sử dụng nhãn được mã hóa để nhân viên có thể tìm bệnh án nhanh chóng."
            }
        },
        "expose": {
            "definition_vi": "cho tiếp xúc với, giúp làm quen/trải nghiệm; phơi bày, vạch trần; để lộ ra",
            "examples_vi": [
                "Các vụ sáp nhập đòi hỏi nhân viên phải được tiếp xúc với những thông lệ kinh doanh khác nhau.",
                "Một tuần làm việc tại mỗi phòng ban của các nhân viên mới đã giúp họ được tiếp cận với các chức năng đa dạng trong công ty."
            ],
            "collocations": [
                "expose sb to sth",
                "be exposed to",
                "media exposure",
                "exposure to sunlight"
            ],
            "usage": {
                "structures": [
                    "expose + sb/sth + to + N (cho ai/cái gì tiếp xúc với cái gì)",
                    "be exposed to + N (được tiếp cận với trải nghiệm mới / bị phơi nhiễm với nhiệt, hóa chất)"
                ],
                "prepositions": ["to"],
                "collocations": [
                    "gain exposure to",
                    "prolonged exposure",
                    "public exposure",
                    "expose a flaw"
                ],
                "tip": "Cả động từ 'expose' và danh từ 'exposure' đều luôn đi kèm với giới từ 'to' (be exposed to / exposure to)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "expose",
                    "example": "The internship program is designed to expose students to international banking.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "exposure",
                    "example": "Positive media exposure helped the startup attract its first thousand customers.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "exposed",
                    "example": "Outdoor electrical cables must be covered so that no wires are left exposed.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The summer internship gives college students valuable _____ to real-world corporate finance.",
                "answer": "exposure",
                "base_word": "expose",
                "pos_hint": "danh từ không đếm được",
                "vi": "Kỳ thực tập mùa hè mang lại cho sinh viên đại học cơ hội tiếp xúc quý giá với ngành tài chính doanh nghiệp thực tế."
            }
        },
        "glimpse": {
            "definition_vi": "cái nhìn thoáng qua, sự trải nghiệm/hiểu biết sơ bộ (n.); nhìn thoáng thấy (v.)",
            "examples_vi": [
                "Cô thư ký đã thoáng nhìn thấy người sếp mới của mình khi bà ấy đang rời khỏi văn phòng.",
                "Sau một năm làm việc tại công ty, anh vẫn cảm thấy như thể mình mới chỉ có một cái nhìn sơ bộ về hoạt động tổng thể."
            ],
            "collocations": [
                "catch a glimpse of",
                "get a glimpse of",
                "a glimpse into",
                "brief glimpse"
            ],
            "usage": {
                "structures": [
                    "catch / get a glimpse of + N (nhìn thoáng thấy / có cái nhìn sơ lược về)",
                    "offer / provide a glimpse into + N (hé lộ cái nhìn về...)"
                ],
                "prepositions": ["of", "into", "at"],
                "collocations": [
                    "rare glimpse",
                    "quick glimpse",
                    "sneak a glimpse",
                    "glimpse the future"
                ],
                "tip": "Ghi nhớ cụm cố định 'catch/get a glimpse of' (nhìn thoáng qua) và 'give/offer a glimpse into' (mang lại góc nhìn hé lộ về điều gì)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "glimpse",
                    "example": "Commuters glimpsed the new high-speed train during its test run this morning.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "glimpse",
                    "example": "The factory tour offers visitors a fascinating glimpse into how cars are built.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The documentary provides viewers with a rare _____ into the daily life of deep-sea researchers.",
                "answer": "glimpse",
                "base_word": "glimpse",
                "pos_hint": "danh từ số ít",
                "vi": "Bộ phim tài liệu mang đến cho khán giả một cái nhìn hiếm hoi về cuộc sống hàng ngày của các nhà nghiên cứu biển sâu."
            }
        },
        "out of": {
            "definition_vi": "hết, cạn kiệt, không còn nữa; ra khỏi",
            "examples_vi": [
                "Các đơn đặt hàng nên được thực hiện trước khi bạn dùng hết sạch văn phòng phẩm.",
                "Người thuyết trình đã hết thời gian trước khi đi đến phần kết luận của mình."
            ],
            "collocations": [
                "run out of",
                "out of stock",
                "out of print",
                "out of order"
            ],
            "usage": {
                "structures": [
                    "run out of + N (dùng hết, cạn kiệt cái gì)",
                    "be out of + N (time / stock / money / work / order)"
                ],
                "prepositions": ["of"],
                "collocations": [
                    "out of business",
                    "out of date",
                    "out of reach",
                    "out of town"
                ],
                "tip": "Các cụm 'run out of (supplies/time)', 'out of stock' (hết hàng), 'out of order' (hỏng máy), 'out of town' (đi vắng) xuất hiện với tần suất dày đặc trong mọi phần thi TOEIC."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "outer",
                    "example": "Please remove the outer packaging before placing the tray in the oven.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "outwardly",
                    "example": "The negotiator remained outwardly calm despite the tense atmosphere.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The vending machine on the third floor is currently _____ of order, so please use the one in the lobby.",
                "answer": "out",
                "base_word": "out of",
                "pos_hint": "giới từ / tính từ (trong cụm 'out of order')",
                "vi": "Máy bán hàng tự động ở tầng ba hiện đang bị hỏng, vì vậy vui lòng sử dụng máy ở sảnh."
            }
        },
        "outdated": {
            "definition_vi": "lỗi thời, lạc hậu, không còn hợp thời/hiệu lực",
            "examples_vi": [
                "Mục đích của buổi hội thảo là để nhân viên xác định các phương pháp và quy trình đã lỗi thời.",
                "Trước khi bạn gửi thư hàng loạt, hãy đảm bảo rằng không có địa chỉ nào bị lỗi thời."
            ],
            "collocations": [
                "outdated equipment",
                "outdated software",
                "outdated methods",
                "replace outdated systems"
            ],
            "usage": {
                "structures": [
                    "be / become / seem + outdated",
                    "outdated + N (equipment / technology / regulations / information)"
                ],
                "prepositions": ["by"],
                "collocations": [
                    "outdated machinery",
                    "outdated policies",
                    "completely outdated",
                    "outdated contact information"
                ],
                "tip": "'Outdated' hoàn toàn đồng nghĩa với 'obsolete' và 'out of date' (lạc hậu, lỗi thời), rất hay gặp trong ngữ cảnh nâng cấp máy móc/quy trình văn phòng."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "outdate",
                    "example": "Rapid advances in artificial intelligence quickly outdate older software tools.",
                    "pos_source": "extended"
                },
                {
                    "pos": "verb",
                    "word": "update",
                    "example": "Please update your emergency contact details on the employee portal.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "outdated",
                    "example": "The factory is replacing its outdated assembly machines with automated robots.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Our accounting department is finally upgrading its _____ computer system next month.",
                "answer": "outdated",
                "base_word": "outdated",
                "pos_hint": "tính từ",
                "vi": "Phòng kế toán của chúng tôi cuối cùng cũng sẽ nâng cấp hệ thống máy tính đã lỗi thời của mình vào tháng tới."
            }
        },
        "practice": {
            "definition_vi": "thói quen, thông lệ, phương pháp làm việc; sự thực hành (n.); luyện tập, thực thi (v.)",
            "examples_vi": [
                "Bà quản lý đã bắt đầu thông lệ tổ chức các cuộc họp ăn sáng hàng tuần từ hơn hai mươi năm trước.",
                "Bill đã luyện tập trả lời điện thoại cho đến khi anh ấy cảm thấy hài lòng."
            ],
            "collocations": [
                "standard practice",
                "best practices",
                "business practices",
                "put into practice"
            ],
            "usage": {
                "structures": [
                    "practice + N / V-ing (luyện tập làm gì - sau practice là V-ing)",
                    "put + N + into practice (đưa ý tưởng/kế hoạch vào thực tiễn)"
                ],
                "prepositions": ["in", "into", "of"],
                "collocations": [
                    "common practice",
                    "in practice",
                    "medical practice",
                    "practical experience"
                ],
                "tip": "Trong TOEIC, danh từ đếm được 'practice(s)' thường không dịch là 'sự luyện tập' mà dịch là 'thông lệ / phương thức làm việc' (standard business practices)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "practitioner",
                    "example": "The conference brings together legal scholars and experienced practitioners.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "practically",
                    "example": "The new high-speed train has practically cut our travel time in half.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "It is standard _____ at our hotel to request a credit card upon check-in for incidental charges.",
                "answer": "practice",
                "base_word": "practice",
                "pos_hint": "danh từ (thông lệ)",
                "vi": "Việc yêu cầu thẻ tín dụng khi nhận phòng để thanh toán các chi phí phát sinh là thông lệ tiêu chuẩn tại khách sạn của chúng tôi."
            }
        },
        "reinforce": {
            "definition_vi": "củng cố, tăng cường, làm vững chắc thêm (ý kiến, kiến thức, kết cấu)",
            "examples_vi": [
                "Phương pháp phân tích dữ liệu khác thường của vị giám đốc tài chính đã được củng cố bởi bài báo trên tạp chí kinh doanh.",
                "Nhân viên đã củng cố những gì họ học được bằng việc thực hành tại nơi làm việc."
            ],
            "collocations": [
                "reinforce a message",
                "reinforce learning",
                "reinforced concrete",
                "mutually reinforcing"
            ],
            "usage": {
                "structures": [
                    "reinforce + N (belief / image / structure / commitment) (with/by + N)"
                ],
                "prepositions": ["with", "by"],
                "collocations": [
                    "reinforce safety rules",
                    "reinforce brand loyalty",
                    "positive reinforcement",
                    "reinforce steel beams"
                ],
                "tip": "Vừa dùng theo nghĩa đen trong xây dựng (reinforce the bridge/concrete: gia cố cầu/bê tông cốt thép) vừa dùng theo nghĩa bóng (reinforce a reputation/idea: củng cố uy tín/quan điểm)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "reinforced",
                    "example": "The warehouse floor is built of reinforced concrete to support heavy forklifts.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Winning the industry award has further _____ our company's reputation for excellence.",
                "answer": "reinforced",
                "base_word": "reinforce",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed)",
                "vi": "Việc giành được giải thưởng của ngành đã củng cố thêm danh tiếng xuất sắc của công ty chúng ta."
            }
        },
        "verbally": {
            "definition_vi": "bằng lời nói, bằng miệng (chứ không phải bằng văn bản)",
            "examples_vi": [
                "Bà đã khiển trách bằng lời đối với nhân viên mới trước mặt toàn bộ nhóm của anh ta.",
                "Lời bảo đảm đó chỉ được đưa ra bằng miệng."
            ],
            "collocations": [
                "verbally agree",
                "verbally notify",
                "communicate verbally",
                "verbal agreement"
            ],
            "usage": {
                "structures": [
                    "verbally + V / V3-ed (verbally agreed / reprimanded / abused)",
                    "V + verbally (communicate / confirm verbally)"
                ],
                "prepositions": ["to", "with"],
                "collocations": [
                    "verbal contract",
                    "verbal warning",
                    "verbal skills",
                    "both verbally and in writing"
                ],
                "tip": "Trong TOEIC, 'verbally' (bằng miệng/lời nói) luôn được đặt đối lập với 'in writing' (bằng văn bản)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "verbalization",
                    "example": "Clear verbalization of safety rules is essential during factory orientations.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Any changes to the project scope must be confirmed in writing rather than just _____.",
                "answer": "verbally",
                "base_word": "verbally",
                "pos_hint": "trạng từ",
                "vi": "Bất kỳ thay đổi nào đối với phạm vi dự án đều phải được xác nhận bằng văn bản chứ không chỉ bằng lời nói."
            }
        }
    },
    9: {
        "disk": {
            "definition_vi": "đĩa máy tính, ổ đĩa (dùng để lưu trữ dữ liệu kỹ thuật số)",
            "examples_vi": [
                "Đầu đọc của ổ đĩa quang đã bị bẩn.",
                "Đĩa компакт (CD) có thể ghi lại đắt hơn so với đĩa CD chỉ đọc."
            ],
            "collocations": [
                "hard disk",
                "disk drive",
                "optical disk",
                "disk space"
            ],
            "usage": {
                "structures": [
                    "save / store (data) on a disk",
                    "hard disk drive (ổ đĩa cứng)"
                ],
                "prepositions": ["on", "from"],
                "collocations": [
                    "external hard disk",
                    "backup disk",
                    "format a disk",
                    "eject a disk"
                ],
                "tip": "Đi kèm với giới từ 'on' khi nói về việc lưu dữ liệu trên ổ đĩa (store files on a hard disk)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "disk",
                    "example": "Please back up your files on an external hard disk before Friday.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "diskette",
                    "example": "Older archival records from the 1990s were originally stored on diskettes.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The computer alerted the user that there was insufficient space on the hard _____ to install the update.",
                "answer": "disk",
                "base_word": "disk",
                "pos_hint": "danh từ số ít",
                "vi": "Máy tính cảnh báo người dùng rằng không còn đủ dung lượng trên ổ đĩa cứng để cài đặt bản cập nhật."
            }
        },
        "facilitate": {
            "definition_vi": "tạo điều kiện thuận lợi, làm cho dễ dàng hơn, thúc đẩy",
            "examples_vi": [
                "Chương trình máy tính đã giúp việc lên lịch hẹn trở nên dễ dàng hơn.",
                "Vị giám đốc đã cố gắng tạo điều kiện thuận lợi cho quá trình chuyển đổi sang chính sách mới bằng cách gặp gỡ tất cả nhân viên sẽ bị ảnh hưởng."
            ],
            "collocations": [
                "facilitate communication",
                "facilitate the process",
                "facilitate trade",
                "workshop facilitator"
            ],
            "usage": {
                "structures": [
                    "facilitate + N (communication / learning / transition / growth)"
                ],
                "prepositions": ["by", "through"],
                "collocations": [
                    "greatly facilitate",
                    "facilitate collaboration",
                    "facilitate the exchange of",
                    "training facilitator"
                ],
                "tip": "Lưu ý: chủ ngữ của 'facilitate' thường là sự vật/công cụ/chính sách, và tân ngữ là một công việc/quá trình (The new software facilitates data sharing), KHÔNG lấy người làm tân ngữ trực tiếp (không viết 'facilitate employees')."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "facilitate",
                    "example": "The new bridge will facilitate trade between the two provinces.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "facilitation",
                    "example": "Trade facilitation measures have reduced customs clearance times.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "facilitator",
                    "example": "We hired an experienced facilitator to lead the strategic planning retreat.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "facilitative",
                    "example": "Modern managers adopt a facilitative approach rather than micromanaging.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The open-plan office layout was designed to _____ communication among different departments.",
                "answer": "facilitate",
                "base_word": "facilitate",
                "pos_hint": "động từ nguyên mẫu (sau 'to')",
                "vi": "Cách bố trí văn phòng không gian mở được thiết kế nhằm tạo điều kiện thuận lợi cho việc giao tiếp giữa các phòng ban khác nhau."
            }
        },
        "network": {
            "definition_vi": "kết nối mạng; giao lưu mở rộng mối quan hệ (v.); mạng lưới (máy tính, truyền hình, quan hệ) (n.)",
            "examples_vi": [
                "Sinh viên mới tốt nghiệp đã giao lưu tạo dựng mối quan hệ với các đồng nghiệp của mẹ cô ấy.",
                "Chúng tôi đã thiết lập một mạng máy tính mới trong văn phòng để chia sẻ tệp tin."
            ],
            "collocations": [
                "computer network",
                "network with peers",
                "networking event",
                "distribution network"
            ],
            "usage": {
                "structures": [
                    "network with + sb (giao lưu kết nối quan hệ công việc với ai)",
                    "set up / build a network"
                ],
                "prepositions": ["with", "of", "on"],
                "collocations": [
                    "wireless network",
                    "professional networking",
                    "network administrator",
                    "global network"
                ],
                "tip": "Trong TOEIC, 'network / networking' ngoài nghĩa 'mạng máy tính' còn cực kỳ phổ biến với nghĩa 'giao lưu mở rộng quan hệ nghề nghiệp' tại các hội nghị."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "network",
                    "example": "Trade shows offer a great opportunity to network with potential clients.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "networking",
                    "example": "A one-hour networking reception will follow the keynote presentation.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "networked",
                    "example": "All of the printers on this floor are networked to the main server.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The evening reception provides an informal setting for conference attendees to _____ with industry leaders.",
                "answer": "network",
                "base_word": "network",
                "pos_hint": "động từ nguyên mẫu (sau 'to')",
                "vi": "Buổi tiệc chiêu đãi tối mang lại một không gian thân mật để những người tham dự hội nghị giao lưu kết nối với các nhà lãnh đạo trong ngành."
            }
        },
        "popularity": {
            "definition_vi": "sự phổ biến, sự được ưa chuộng rộng rãi",
            "examples_vi": [
                "Sau khi các quảng cáo mới bắt đầu phát sóng, mức độ ưa chuộng của loại pin này đã tăng lên đáng kể.",
                "Thương hiệu máy tính này cực kỳ phổ biến trong giới sinh viên đại học."
            ],
            "collocations": [
                "gain popularity",
                "grow in popularity",
                "enjoy great popularity",
                "popular among / with"
            ],
            "usage": {
                "structures": [
                    "gain / grow / increase in popularity (ngày càng được ưa chuộng)",
                    "be popular with / among + đối tượng khách hàng"
                ],
                "prepositions": ["of", "in", "with", "among"],
                "collocations": [
                    "widespread popularity",
                    "declining popularity",
                    "popular demand",
                    "immensely popular"
                ],
                "tip": "Tính từ 'popular' đi với giới từ 'with' hoặc 'among' (popular with young commuters), còn danh từ 'popularity' rất hay đi với cụm 'grow/increase IN popularity'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "popularly",
                    "example": "The historic district is popularly known as the Old Quarter.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Electric scooters have grown rapidly in _____ among urban commuters over the past two years.",
                "answer": "popularity",
                "base_word": "popularity",
                "pos_hint": "danh từ (sau giới từ 'in')",
                "vi": "Xe trượt điện đã tăng nhanh về mức độ phổ biến trong giới người đi làm ở đô thị suốt hai năm qua."
            }
        },
        "process": {
            "definition_vi": "xử lý (dữ liệu, đơn hàng, hồ sơ), chế biến (v.); quy trình, quá trình (n.)",
            "examples_vi": [
                "Tôi đã xử lý xong dữ liệu mình thu thập được và thu về một số kết quả thú vị.",
                "Có một quy trình để xác định lý do tại sao máy tính của bạn lại gặp trục trặc."
            ],
            "collocations": [
                "in the process of",
                "process an order",
                "hiring process",
                "data processing"
            ],
            "usage": {
                "structures": [
                    "be in the process of + V-ing (đang trong quá trình làm gì)",
                    "process + N (application / refund / order / payment / data)"
                ],
                "prepositions": ["in", "of", "for"],
                "collocations": [
                    "word processor",
                    "manufacturing process",
                    "selection process",
                    "processed food"
                ],
                "tip": "Động từ 'process' xuất hiện cực nhiều trong ngữ cảnh hành chính/thương mại điện tử: 'Please allow 5 business days for your refund/application/order to be processed'."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "process",
                    "example": "It takes three business days to process a passport renewal application.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "processor",
                    "example": "The new laptop is equipped with an ultra-fast quad-core processor.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "processing",
                    "example": "A small processing fee is charged for all international wire transfers.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "processed",
                    "example": "All processed orders are shipped from our warehouse within 24 hours.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Please allow up to seven business days for your reimbursement request to be _____.",
                "answer": "processed",
                "base_word": "process",
                "pos_hint": "động từ chia quá khứ phân từ (V3/ed - bị động)",
                "vi": "Vui lòng chờ tối đa bảy ngày làm việc để yêu cầu hoàn trả chi phí của bạn được xử lý."
            }
        },
        "replace": {
            "definition_vi": "thay thế (vật hỏng, người nghỉ việc); đặt lại chỗ cũ",
            "examples_vi": [
                "Tôi đã thay thế ổ cứng bị trục trặc.",
                "Chúng tôi đã tìm kiếm trong ba tháng và vẫn chưa tìm được ai có thể thay thế cho người quản trị viên trước đây của chúng tôi."
            ],
            "collocations": [
                "replace A with B",
                "replacement parts",
                "find a replacement",
                "easily replaceable"
            ],
            "usage": {
                "structures": [
                    "replace A with/by B (thay thế cái cũ A bằng cái mới B)",
                    "a replacement for + A (người/vật thay thế cho A)"
                ],
                "prepositions": ["with", "by", "for"],
                "collocations": [
                    "battery replacement",
                    "free replacement",
                    "irreplaceable asset",
                    "replacement cost"
                ],
                "tip": "Động từ 'replace' đi với giới từ 'with' (replace old monitors WITH flat screens), nhưng danh từ 'replacement' đi với giới từ 'for' (a replacement FOR the retiring director)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "irreplaceable",
                    "example": "Her twenty years of institutional knowledge made her nearly irreplaceable.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "If your appliance stops working during the warranty period, we will send you a _____ free of charge.",
                "answer": "replacement",
                "base_word": "replace",
                "pos_hint": "danh từ số ít",
                "vi": "Nếu thiết bị của bạn ngừng hoạt động trong thời gian bảo hành, chúng tôi sẽ gửi cho bạn một sản phẩm thay thế miễn phí."
            }
        },
        "revolution": {
            "definition_vi": "cuộc cách mạng, sự thay đổi mang tính đột phá; một vòng quay trọn vẹn",
            "examples_vi": [
                "Chúng ta chứng kiến một cuộc cách mạng trong lĩnh vực máy tính gần như mỗi ngày.",
                "Đầu đĩa CD của tôi bị hỏng; chiếc đĩa không thể quay trọn một vòng quanh nam châm."
            ],
            "collocations": [
                "technological revolution",
                "industrial revolution",
                "revolutionary design",
                "revolutionize the industry"
            ],
            "usage": {
                "structures": [
                    "a revolution in + lĩnh vực (cuộc cách mạng trong ngành gì)",
                    "revolutionize + N (cách mạng hóa ngành/lĩnh vực gì)"
                ],
                "prepositions": ["in", "around"],
                "collocations": [
                    "digital revolution",
                    "complete revolution",
                    "revolutionary product",
                    "revolutionary approach"
                ],
                "tip": "Tính từ 'revolutionary' (mang tính cách mạng/đột phá) là từ rất được ưa chuộng trong các bài quảng cáo sản phẩm công nghệ mới của TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "revolutionize",
                    "example": "Cloud computing has revolutionized the way small businesses manage data.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The company's _____ new battery technology allows electric cars to charge in just ten minutes.",
                "answer": "revolutionary",
                "base_word": "revolution",
                "pos_hint": "tính từ",
                "vi": "Công nghệ pin mới mang tính cách mạng của công ty cho phép ô tô điện sạc chỉ trong mười phút."
            }
        },
        "sharp": {
            "definition_vi": "đột ngột, mạnh (tăng/giảm); nhạy bén, thông minh; sắc bén, rõ nét; đúng giờ",
            "examples_vi": [
                "Đã có một sự sụt giảm mạnh về số lượng cuộc gọi đến bàn trợ giúp sau khi chúng tôi nâng cấp máy tính của từng nhân viên.",
                "Nhân viên mới đã chứng minh cô ấy nhạy bén đến mức nào khi làm chủ được chương trình mới chỉ trong vài ngày."
            ],
            "collocations": [
                "sharp decline / drop",
                "sharp increase / rise",
                "at 9 o'clock sharp",
                "sharply higher"
            ],
            "usage": {
                "structures": [
                    "a sharp + N (increase / rise / decline / drop / contrast) (tăng/giảm đột ngột)",
                    "rise / fall / drop + sharply (tăng/giảm mạnh)",
                    "at + giờ + sharp (đúng chính xác mấy giờ)"
                ],
                "prepositions": ["in", "at"],
                "collocations": [
                    "sharp contrast",
                    "sharpen skills",
                    "sharp mind",
                    "sharp image"
                ],
                "tip": "Trong TOEIC, 'sharp / sharply' cực kỳ hay đi kèm với các từ chỉ sự biến động số liệu như 'increase, rise, drop, decline, fall' (tăng/giảm mạnh và đột ngột)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "sharpen",
                    "example": "The workshop is designed to help managers sharpen their leadership skills.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "sharpness",
                    "example": "The new monitor offers exceptional color accuracy and image sharpness.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "sharp",
                    "example": "There was a sharp rise in online orders during the fourth quarter.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "sharply",
                    "example": "Raw material prices have risen sharply over the past six months.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Attendance at the museum rose _____ after the new dinosaur exhibit opened in June.",
                "answer": "sharply",
                "base_word": "sharp",
                "pos_hint": "trạng từ (bổ nghĩa cho động từ 'rose')",
                "vi": "Lượng khách tham quan bảo tàng đã tăng vọt sau khi cuộc triển lãm khủng long mới mở cửa vào tháng Sáu."
            }
        },
        "skill": {
            "definition_vi": "kỹ năng, sự khéo léo, tay nghề",
            "examples_vi": [
                "Nhà phát triển phần mềm có kỹ năng kỹ thuật xuất sắc và sẽ là một tài sản quý giá cho nhóm lập trình phần mềm của chúng ta.",
                "Công việc thiết kế dụng cụ điện tử của Salman tận dụng rất tốt kỹ năng khéo léo đôi tay của anh ấy."
            ],
            "collocations": [
                "communication skills",
                "technical skills",
                "skilled workers",
                "interpersonal skills"
            ],
            "usage": {
                "structures": [
                    "be skilled in / at + N/V-ing (có tay nghề/giỏi về việc gì)",
                    "acquire / develop / hone skills"
                ],
                "prepositions": ["in", "at"],
                "collocations": [
                    "highly skilled",
                    "management skills",
                    "computer skills",
                    "skillful negotiator"
                ],
                "tip": "Tính từ 'skilled' (có tay nghề cao, lành nghề) thường đi với giới từ 'in' hoặc 'at' (skilled in negotiation) hoặc đứng trước danh từ chỉ người (skilled technicians)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "skillful",
                    "example": "Thanks to her skillful handling of the crisis, the company avoided a lawsuit.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The shipyard is currently recruiting _____ welders and electricians for a major contract.",
                "answer": "skilled",
                "base_word": "skill",
                "pos_hint": "tính từ",
                "vi": "Xưởng đóng tàu hiện đang tuyển dụng những thợ hàn và thợ điện lành nghề cho một hợp đồng lớn."
            }
        },
        "software": {
            "definition_vi": "phần mềm máy tính, chương trình máy tính",
            "examples_vi": [
                "Phần mềm này cho phép tôi tích hợp các bảng biểu và bảng tính vào báo cáo của mình.",
                "Nhiều máy tính được cài đặt sẵn phần mềm khi xuất xưởng."
            ],
            "collocations": [
                "software application",
                "accounting software",
                "software developer",
                "install software"
            ],
            "usage": {
                "structures": [
                    "install / update / upgrade software (luôn là danh từ KHÔNG đếm được)",
                    "a piece of software / a software program (khi muốn đếm số lượng)"
                ],
                "prepositions": ["on", "for"],
                "collocations": [
                    "antivirus software",
                    "proprietary software",
                    "software update",
                    "software engineering"
                ],
                "tip": "Bẫy ngữ pháp: 'software' (cũng như hardware, equipment, information) là danh từ KHÔNG đếm được, không bao giờ có 'a software' hay 'softwares'."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "software",
                    "example": "All employees must install the latest security software on their laptops.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "ware",
                    "example": "The artisan market features locally crafted glassware and ceramic wares.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Our IT department will install the new accounting _____ on all office computers this weekend.",
                "answer": "software",
                "base_word": "software",
                "pos_hint": "danh từ không đếm được",
                "vi": "Bộ phận công nghệ thông tin của chúng tôi sẽ cài đặt phần mềm kế toán mới trên tất cả máy tính văn phòng vào cuối tuần này."
            }
        },
        "store": {
            "definition_vi": "lưu trữ, cất giữ, tích trữ (v.); cửa hàng; kho dự trữ (n.)",
            "examples_vi": [
                "Bạn có thể lưu trữ nhiều dữ liệu hơn trên ổ đĩa zip.",
                "Chúng tôi cất giữ các đĩa gốc trong két sắt chống cháy."
            ],
            "collocations": [
                "store data",
                "storage space",
                "storage facility",
                "in storage"
            ],
            "usage": {
                "structures": [
                    "store + N (data / supplies / luggage) + in/on + địa điểm",
                    "put / keep + N + in storage (cất giữ trong kho)"
                ],
                "prepositions": ["in", "on", "at"],
                "collocations": [
                    "cold storage",
                    "cloud storage",
                    "storage capacity",
                    "department store"
                ],
                "tip": "Danh từ không đếm được 'storage' (sự lưu trữ / kho chứa / dung lượng lưu trữ) xuất hiện rất thường xuyên trong các cụm 'storage space, storage room, cloud storage'."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "storable",
                    "example": "Freeze-dried meals are lightweight and easily storable for months.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The office leased an off-site _____ unit to keep archival tax documents and extra furniture.",
                "answer": "storage",
                "base_word": "store",
                "pos_hint": "danh từ (làm định ngữ cho 'unit')",
                "vi": "Văn phòng đã thuê một kho lưu trữ bên ngoài để cất giữ các tài liệu thuế lưu trữ và đồ nội thất dư thừa."
            }
        },
        "technically": {
            "definition_vi": "về mặt kỹ thuật/chuyên môn; xét theo lý thuyết/quy định chặt chẽ",
            "examples_vi": [
                "Xét về mặt kỹ thuật, loại vi-rút này chỉ lây nhiễm vào các tệp kịch bản (script).",
                "Văn phòng cuối cùng cũng đã bắt kịp tiến độ về mặt kỹ thuật."
            ],
            "collocations": [
                "technically speaking",
                "technically advanced",
                "technical support",
                "technical difficulties"
            ],
            "usage": {
                "structures": [
                    "Technically (speaking), + mệnh đề (Xét về mặt lý thuyết/quy định chặt chẽ thì...)",
                    "technically + Adj/V3-ed (technically demanding / advanced / qualified)"
                ],
                "prepositions": ["in"],
                "collocations": [
                    "technical specifications",
                    "technical expertise",
                    "minor technicality",
                    "technical manual"
                ],
                "tip": "Chú ý cụm danh từ cực kỳ phổ biến 'technical support' (hỗ trợ kỹ thuật) và 'technical specifications' (thông số kỹ thuật)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "technician",
                    "example": "A certified technician will arrive tomorrow to repair the photocopier.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The live webinar was delayed by fifteen minutes due to unexpected _____ difficulties.",
                "answer": "technical",
                "base_word": "technically",
                "pos_hint": "tính từ",
                "vi": "Buổi hội thảo trực tuyến đã bị trễ mười lăm phút do những sự cố kỹ thuật ngoài dự kiến."
            }
        }
    },
    10: {
        "assemble": {
            "definition_vi": "lắp ráp (máy móc, đồ đạc), tập hợp/gom lại (tài liệu, con người)",
            "examples_vi": [
                "Trợ lý của bà đã sao chụp và tập hợp các tài liệu lại với nhau.",
                "Nhân viên phòng văn thư đã đọc kỹ hướng dẫn trước khi lắp ráp các bộ phận của chiếc máy in bưu phí mới."
            ],
            "collocations": [
                "assemble furniture",
                "assemble documents",
                "assembly line",
                "easily assembled"
            ],
            "usage": {
                "structures": [
                    "assemble + N (parts / furniture / team / data)",
                    "assemble in + địa điểm (tập trung tại đâu)"
                ],
                "prepositions": ["in", "from"],
                "collocations": [
                    "assembly plant",
                    "some assembly required",
                    "assembly instructions",
                    "fully assembled"
                ],
                "tip": "Danh từ 'assembly' (sự lắp ráp / dây chuyền lắp ráp: assembly line) là từ vựng cốt lõi trong chủ đề Manufacturing (Sản xuất) của TOEIC."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "assemble",
                    "example": "It took two hours to assemble the new office bookshelves.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "assembly",
                    "example": "The bookcase comes with step-by-step assembly instructions.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "assembled",
                    "example": "The desk is shipped fully assembled so no tools are required.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Automated robots on the _____ line have doubled the factory's daily output.",
                "answer": "assembly",
                "base_word": "assemble",
                "pos_hint": "danh từ (trong cụm 'assembly line')",
                "vi": "Những robot tự động trên dây chuyền lắp ráp đã làm tăng gấp đôi sản lượng hàng ngày của nhà máy."
            }
        },
        "beforehand": {
            "definition_vi": "trước, từ trước, sẵn từ trước (= in advance)",
            "examples_vi": [
                "Để đẩy nhanh việc gửi thư, chúng ta nên chuẩn bị sẵn các nhãn dán từ trước.",
                "Hàng hóa lẽ ra đã có thể được vận chuyển ngay hôm nay nếu họ gửi fax đơn đặt hàng từ trước."
            ],
            "collocations": [
                "prepare beforehand",
                "notify sb beforehand",
                "know beforehand",
                "arrange beforehand"
            ],
            "usage": {
                "structures": [
                    "V + (O) + beforehand (thường đứng ở cuối mệnh đề)"
                ],
                "prepositions": [],
                "collocations": [
                    "book beforehand",
                    "register beforehand",
                    "check beforehand",
                    "days beforehand"
                ],
                "tip": "Trạng từ 'beforehand' hoàn toàn đồng nghĩa với cụm 'in advance' hoặc 'ahead of time' (làm sẵn từ trước) và thường đứng ở cuối câu."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "beforehand",
                    "example": "Being beforehand with our tax filings saved the firm from late penalties.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "beforehand",
                    "example": "If you need a projector for your presentation, please let us know beforehand.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "To avoid long lines at the venue, visitors are advised to purchase their tickets _____.",
                "answer": "beforehand",
                "base_word": "beforehand",
                "pos_hint": "trạng từ",
                "vi": "Để tránh phải xếp hàng dài tại địa điểm tổ chức, du khách được khuyên nên mua vé trước."
            }
        },
        "complication": {
            "definition_vi": "sự phức tạp, rắc rối phát sinh; biến chứng (y khoa)",
            "examples_vi": [
                "Cô ấy sẽ phải ở lại bệnh viện thêm hai ngày do những biến chứng trong quá trình phẫu thuật.",
                "Những rắc rối phức tạp luôn nảy sinh khi chúng ta cố gắng đề cập quá nhiều chủ đề trong cùng một bức thư."
            ],
            "collocations": [
                "avoid complications",
                "unforeseen complications",
                "further complications",
                "complicate matters"
            ],
            "usage": {
                "structures": [
                    "complications arise / occur (những rắc rối phát sinh - thường dùng ở số nhiều)",
                    "be complicated by + N (bị làm cho phức tạp bởi)"
                ],
                "prepositions": ["with", "in", "by"],
                "collocations": [
                    "without complication",
                    "legal complications",
                    "complicated procedure",
                    "unnecessarily complicated"
                ],
                "tip": "Danh từ 'complication(s)' thường dùng ở dạng số nhiều để chỉ 'những rắc rối/trở ngại phát sinh làm mọi việc khó khăn hơn'."
            },
            "extra_families": [
                {
                    "pos": "adverb",
                    "word": "complicatedly",
                    "example": "The tax form was so complicatedly worded that we had to hire an accountant.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The new online tax filing system is much less _____ than the old paper-based method.",
                "answer": "complicated",
                "base_word": "complication",
                "pos_hint": "tính từ",
                "vi": "Hệ thống khai thuế trực tuyến mới ít phức tạp hơn nhiều so với phương pháp trên giấy cũ."
            }
        },
        "courier": {
            "definition_vi": "nhân viên/dịch vụ chuyển phát nhanh, người đưa thư tín/bưu kiện",
            "examples_vi": [
                "Chúng tôi đã thuê một người chuyển phát nhanh để giao kiện hàng.",
                "Dịch vụ chuyển phát nhanh sẽ làm thủ tục thông quan cho lô hàng."
            ],
            "collocations": [
                "by courier",
                "courier service",
                "overnight courier",
                "express courier"
            ],
            "usage": {
                "structures": [
                    "send / deliver + sth + by courier (gửi cái gì bằng dịch vụ chuyển phát nhanh)"
                ],
                "prepositions": ["by", "via"],
                "collocations": [
                    "bicycle courier",
                    "international courier",
                    "courier company",
                    "dispatch a courier"
                ],
                "tip": "Cụm giới từ 'by courier' (bằng chuyển phát nhanh - không có mạo từ a/the ở giữa) rất hay xuất hiện trong các câu hỏi về giao nhận tài liệu khẩn."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "courier",
                    "example": "We had the signed contracts couriered directly to the client's headquarters.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "courier",
                    "example": "The legal documents were sent by overnight courier this morning.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Because the blueprints were needed urgently, the architect sent them by overnight _____.",
                "answer": "courier",
                "base_word": "courier",
                "pos_hint": "danh từ",
                "vi": "Bởi vì bản thiết kế được cần gấp, kiến trúc sư đã gửi chúng bằng dịch vụ chuyển phát nhanh qua đêm."
            }
        },
        "express": {
            "definition_vi": "tốc hành, nhanh và trực tiếp (adj./adv.); bày tỏ, biểu đạt (v.)",
            "examples_vi": [
                "Điều quan trọng là tài liệu này phải có mặt ở đó vào ngày mai, vì vậy vui lòng gửi nó qua thư chuyển phát nhanh.",
                "Thư chuyển phát nhanh tốn kém hơn dịch vụ bưu chính thông thường, nhưng lại hiệu quả hơn."
            ],
            "collocations": [
                "express mail",
                "express delivery",
                "express train",
                "express gratitude"
            ],
            "usage": {
                "structures": [
                    "express + N (mail / delivery / shipping / lane / train) (tốc hành/nhanh)",
                    "express + N (appreciation / concern / interest / gratitude) (bày tỏ)"
                ],
                "prepositions": ["by", "to"],
                "collocations": [
                    "send by express mail",
                    "express checkout",
                    "express one's opinion",
                    "for the express purpose of"
                ],
                "tip": "Từ 'express' vừa là tính từ mang nghĩa 'tốc hành/nhanh' (express delivery/train), vừa là động từ rất phổ biến mang nghĩa 'bày tỏ' (express concern/appreciation)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "express",
                    "example": "Several board members expressed concern about the rising construction costs.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "expression",
                    "example": "Please accept this gift basket as an expression of our gratitude.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "expressive",
                    "example": "The actor is known for his expressive voice and commanding stage presence.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adverb",
                    "word": "expressly",
                    "example": "The company car is to be used expressly for official business purposes.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Duplicating any part of this manual without the _____ written permission of the publisher is prohibited.",
                "answer": "express",
                "base_word": "express",
                "pos_hint": "tính từ (rõ ràng, đích xác)",
                "vi": "Việc sao chép bất kỳ phần nào của cuốn cẩm nang này mà không có sự cho phép rõ ràng bằng văn bản của nhà xuất bản đều bị nghiêm cấm."
            }
        },
        "fold": {
            "definition_vi": "gấp, gập lại (giấy, quần áo, ghế) (v.); nếp gấp (n.)",
            "examples_vi": [
                "Hãy gấp bức thư làm ba phần trước khi cho vào phong bì.",
                "Đừng gấp tài liệu lại nếu nó không vừa với chiếc phong bì."
            ],
            "collocations": [
                "fold a letter",
                "fold in half",
                "folding chair",
                "twofold increase"
            ],
            "usage": {
                "structures": [
                    "fold + N + in half / into three parts (gấp đôi / gấp làm ba)",
                    "fold up + N (gập gọn lại)"
                ],
                "prepositions": ["in", "into", "up"],
                "collocations": [
                    "do not fold or bend",
                    "folding table",
                    "foldable bicycle",
                    "threefold"
                ],
                "tip": "Trong TOEIC Part 1 (Mô tả tranh), chú ý phân biệt 'folding chairs' (những chiếc ghế xếp) và 'folded clothes/towels' (quần áo/khăn đã được gấp gọn)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "fold",
                    "example": "The brochures are printed and folded automatically by the new machine.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "folder",
                    "example": "Please place all expense receipts inside the blue file folder.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "foldable",
                    "example": "The commuter scooter is lightweight and easily foldable for train travel.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The janitor stacked the _____ chairs against the wall after the seminar ended.",
                "answer": "folding",
                "base_word": "fold",
                "pos_hint": "tính từ / phân từ (trong cụm 'folding chairs': ghế xếp)",
                "vi": "Người lao công đã xếp chồng những chiếc ghế gấp sát vào tường sau khi buổi hội thảo kết thúc."
            }
        },
        "layout": {
            "definition_vi": "bố cục, cách trình bày (trang giấy, trang web); sơ đồ bố trí mặt bằng (văn phòng, nhà máy)",
            "examples_vi": [
                "Chúng tôi đã phải thay đổi bố cục trình bày khi thay đổi kích cỡ của khổ giấy.",
                "Bản thiết kế bố cục cho cuốn sách quảng cáo mới đã được nhà thiết kế đệ trình."
            ],
            "collocations": [
                "page layout",
                "office layout",
                "change the layout",
                "approve the layout"
            ],
            "usage": {
                "structures": [
                    "the layout of / for + N (bố cục/sơ đồ bố trí của cái gì)"
                ],
                "prepositions": ["of", "for"],
                "collocations": [
                    "magazine layout",
                    "store layout",
                    "open-plan layout",
                    "keyboard layout"
                ],
                "tip": "Chú ý: viết liền 'layout' là danh từ (bố cục trang in / sơ đồ mặt bằng văn phòng), còn viết tách 'lay out' là cụm động từ (trình bày / sắp đặt)."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "lay",
                    "example": "The proposal clearly lays out the timeline for the construction project.",
                    "pos_source": "extended"
                },
                {
                    "pos": "noun",
                    "word": "layout",
                    "example": "The supermarket redesigned its store layout to make the aisles wider.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "The editor asked the graphic designer to revise the _____ of the magazine's cover page.",
                "answer": "layout",
                "base_word": "layout",
                "pos_hint": "danh từ số ít",
                "vi": "Biên tập viên đã yêu cầu nhà thiết kế đồ họa chỉnh sửa lại bố cục trang bìa của tạp chí."
            }
        },
        "mention": {
            "definition_vi": "sự đề cập, sự nhắc đến (n.); đề cập, nói đến, nhắc tới (v.)",
            "examples_vi": [
                "Không hề có sự đề cập nào về chi phí trong bản đề xuất.",
                "Bạn nên đề cập trong bức thư rằng chúng ta có thể thu xếp cả việc gửi bưu điện lẫn việc in ấn các cuốn sách quảng cáo đó."
            ],
            "collocations": [
                "make mention of",
                "no mention of",
                "not to mention",
                "fail to mention"
            ],
            "usage": {
                "structures": [
                    "mention + N / V-ing / that + mệnh đề (động từ 'mention' KHÔNG đi với giới từ 'about' hay 'to sb')",
                    "make (no) mention of + N (danh từ 'mention' đi với giới từ 'of')"
                ],
                "prepositions": ["of", "in"],
                "collocations": [
                    "as mentioned above",
                    "worth mentioning",
                    "briefly mention",
                    "honorable mention"
                ],
                "tip": "Cụm 'As mentioned in my previous email...' (Như đã đề cập trong email trước của tôi...) là câu mở đầu kinh điển trong các bài đọc thư tín (Part 6 & 7)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "mentioned",
                    "example": "Please send the above-mentioned documents to our legal department.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "As _____ in the attached memorandum, the parking lot will be repaved this Saturday.",
                "answer": "mentioned",
                "base_word": "mention",
                "pos_hint": "quá khứ phân từ (V3/ed - rút gọn mệnh đề bị động)",
                "vi": "Như đã được đề cập trong bản thông báo đính kèm, bãi đỗ xe sẽ được trải nhựa lại vào thứ Bảy này."
            }
        },
        "petition": {
            "definition_vi": "đơn kiến nghị, thư thỉnh cầu có nhiều chữ ký (n.); kiến nghị, làm đơn thỉnh cầu (v.)",
            "examples_vi": [
                "Đơn kiến nghị đã được sao chụp và phát cho các công nhân, những người sẽ thu thập các chữ ký cần thiết.",
                "Chúng tôi đã kiến nghị lên các quan chức bưu điện để bắt đầu giao thư hai lần một ngày tại các khu vực kinh doanh."
            ],
            "collocations": [
                "sign a petition",
                "submit a petition",
                "file a petition",
                "petition for change"
            ],
            "usage": {
                "structures": [
                    "sign / circulate / submit a petition (for/against + N)",
                    "petition + sb + to V / for + N (kiến nghị ai làm gì)"
                ],
                "prepositions": ["for", "against", "to"],
                "collocations": [
                    "online petition",
                    "petition drive",
                    "gather signatures for a petition",
                    "petition the government"
                ],
                "tip": "Danh từ 'petition' rất hay đi kèm với các từ như 'signatures' (chữ ký), 'sign' (ký tên), 'residents/workers' (cư dân/công nhân)."
            },
            "extra_families": [
                {
                    "pos": "adjective",
                    "word": "petitionary",
                    "example": "The union submitted a petitionary letter requesting safer working conditions.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Over three thousand local residents signed a _____ opposing the construction of the highway.",
                "answer": "petition",
                "base_word": "petition",
                "pos_hint": "danh từ số ít",
                "vi": "Hơn ba nghìn cư dân địa phương đã ký vào một lá đơn kiến nghị phản đối việc xây dựng đường cao tốc."
            }
        },
        "proof": {
            "definition_vi": "đọc soát lỗi (bản in/văn bản) (v.); bằng chứng, chứng từ xác nhận (n.); chống thấm/chống chịu được (adj.)",
            "examples_vi": [
                "Bức thư này đã không được đọc soát lỗi cẩn thận; nó có đầy lỗi đánh máy.",
                "Để nhận được khoản tiền hoàn lại (rebate), bạn phải gửi kèm bằng chứng mua hàng."
            ],
            "collocations": [
                "proof of purchase",
                "proof of identity",
                "proofread a document",
                "conclusive proof"
            ],
            "usage": {
                "structures": [
                    "proof of + N (purchase / delivery / payment / identity / residency)",
                    "proof / proofread + a document (đọc dò lỗi văn bản)"
                ],
                "prepositions": ["of"],
                "collocations": [
                    "waterproof",
                    "fireproof",
                    "foolproof",
                    "provide proof"
                ],
                "tip": "Cụm danh từ cố định 'proof of purchase' (bằng chứng mua hàng = hóa đơn/biên lai) xuất hiện trong hầu hết các bài đọc về bảo hành, đổi trả hàng hoặc hoàn tiền."
            },
            "extra_families": [
                {
                    "pos": "verb",
                    "word": "proofread",
                    "example": "Please ask a colleague to proofread your report before sending it to the client.",
                    "pos_source": "extended"
                },
                {
                    "pos": "adjective",
                    "word": "proven",
                    "example": "We are looking for a sales director with a proven track record of success.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Customers must present valid _____ of purchase, such as a store receipt, to claim a refund.",
                "answer": "proof",
                "base_word": "proof",
                "pos_hint": "danh từ không đếm được",
                "vi": "Khách hàng phải xuất trình bằng chứng mua hàng hợp lệ, chẳng hạn như biên lai của cửa hàng, để yêu cầu hoàn tiền."
            }
        },
        "register": {
            "definition_vi": "gửi bảo đảm (thư từ, bưu kiện), đăng ký, ghi vào sổ theo dõi (v.); sổ ghi chép (n.)",
            "examples_vi": [
                "Bạn có thể gửi bảo đảm bức thư này với khoản phí trả thêm là 2,20 đô la.",
                "Mọi người cần phải ký tên vào sổ theo dõi trước khi bước vào phòng văn thư."
            ],
            "collocations": [
                "registered mail",
                "sign the register",
                "register a package",
                "register a complaint"
            ],
            "usage": {
                "structures": [
                    "send + sth + by registered mail (gửi thư bảo đảm)",
                    "sign the register (ký vào sổ ra vào/sổ theo dõi)"
                ],
                "prepositions": ["by", "in", "for"],
                "collocations": [
                    "registered letter",
                    "registered trademark",
                    "visitor register",
                    "cash register"
                ],
                "tip": "Trong chủ đề Correspondence (Thư tín), 'registered mail' có nghĩa là 'thư bảo đảm' (thư có mã theo dõi và yêu cầu người nhận ký nhận)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "registry",
                    "example": "All commercial vessels must be listed in the national shipping registry.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Important legal contracts should always be sent by _____ mail so that delivery can be tracked.",
                "answer": "registered",
                "base_word": "register",
                "pos_hint": "tính từ (V3/ed)",
                "vi": "Các hợp đồng pháp lý quan trọng luôn nên được gửi bằng thư bảo đảm để có thể theo dõi quá trình giao nhận."
            }
        },
        "revise": {
            "definition_vi": "chỉnh sửa, sửa đổi, hiệu đính (văn bản, kế hoạch, dự toán, lịch trình)",
            "examples_vi": [
                "Cuốn sách quảng cáo đã được chỉnh sửa vài lần trước khi được gửi đến nhà in.",
                "Chúng ta sẽ cần phải sửa lại bức thư mẫu vì địa chỉ của chúng ta đã thay đổi."
            ],
            "collocations": [
                "revise a draft",
                "revise an estimate",
                "make revisions",
                "revised edition"
            ],
            "usage": {
                "structures": [
                    "revise + N (document / budget / schedule / forecast)",
                    "make revisions to + N (thực hiện các chỉnh sửa đối với cái gì)"
                ],
                "prepositions": ["to", "for"],
                "collocations": [
                    "revised schedule",
                    "revised budget",
                    "undergo revision",
                    "upward revision"
                ],
                "tip": "Tính từ phân từ 'revised' rất hay đứng trước danh từ chỉ tài liệu/kế hoạch: 'a revised schedule / budget / draft / contract' (lịch trình/ngân sách/bản thảo đã được cập nhật sửa đổi)."
            },
            "extra_families": [
                {
                    "pos": "noun",
                    "word": "reviser",
                    "example": "The publishing house hired an experienced reviser to update the textbook.",
                    "pos_source": "extended"
                }
            ],
            "srs_sentence": {
                "en": "Please review the _____ project timeline and let me know if the new deadlines are feasible.",
                "answer": "revised",
                "base_word": "revise",
                "pos_hint": "tính từ (quá khứ phân từ V3/ed bổ nghĩa cho 'timeline')",
                "vi": "Vui lòng xem lại tiến độ dự án đã được điều chỉnh và cho tôi biết liệu các hạn chót mới có khả thi hay không."
            }
        }
    }
}

if __name__ == "__main__":
    import json

    json_path = r"C:\Users\LEGION\.gemini\antigravity\brain\dd06d532-873e-4cf4-997f-622fdb86edbc\scratch\batch_1.json"
    with open(json_path, "r", encoding="utf-8") as f:
        source_data = json.load(f)

    assert len(BATCH_DATA) == 10, f"Expected 10 lessons, got {len(BATCH_DATA)}"
    total_words = 0
    required_keys = {
        "definition_vi",
        "examples_vi",
        "collocations",
        "usage",
        "extra_families",
        "srs_sentence",
    }

    for lesson_str, lesson_obj in source_data.items():
        lesson_id = int(lesson_str)
        assert lesson_id in BATCH_DATA, f"Missing lesson {lesson_id}"
        lesson_dict = BATCH_DATA[lesson_id]
        assert len(lesson_dict) == 12, f"Lesson {lesson_id} expected 12 words, got {len(lesson_dict)}"

        for w_obj in lesson_obj["words"]:
            w = w_obj["word"]
            assert w in lesson_dict, f"Lesson {lesson_id} missing word '{w}'"
            entry = lesson_dict[w]
            assert required_keys.issubset(entry.keys()), f"Word '{w}' missing keys"
            assert entry["definition_vi"].strip(), f"Empty definition_vi for '{w}'"
            assert len(entry["examples_vi"]) == len(w_obj["examples"]), f"examples_vi count mismatch for '{w}'"
            assert len(entry["collocations"]) >= 4, f"Need >=4 collocations for '{w}'"
            usage = entry["usage"]
            assert usage["structures"] and usage["collocations"] and usage["tip"], f"Incomplete usage for '{w}'"
            srs = entry["srs_sentence"]
            assert "_____" in srs["en"], f"Missing blank in srs_sentence for '{w}'"
            assert srs["answer"].strip() and srs["base_word"] == w and srs["pos_hint"].strip() and srs["vi"].strip()
            total_words += 1

    print(f"SUCCESS: Verified {len(BATCH_DATA)} lessons and {total_words} words in vocab_data_batch1.py!")
