import sys

class LanguageAgent:
    """
    Language Intelligence Agent detects targets and translates disaster reports,
    EOC command headers, safety directives, and contact panels into 11 regional languages.
    """

    # Language code mapping mapping locale to display name
    LANGUAGES = {
        "en": "English",
        "hi": "हिन्दी (Hindi)",
        "pa": "ਪੰਜਾਬੀ (Punjabi)",
        "ta": "தமிழ் (Tamil)",
        "te": "తెలుగు (Telugu)",
        "bn": "বাংলা (Bengali)",
        "mr": "मराठी (Marathi)",
        "gu": "ગુજરાતી (Gujarati)",
        "kn": "ಕನ್ನಡ (Kannada)",
        "ml": "മലയാളം (Malayalam)",
        "ur": "اردو (Urdu)"
    }

    # ISO Language TTS Codes for HTML5 Speak Utterances
    TTS_LOCALE = {
        "en": "en-US",
        "hi": "hi-IN",
        "pa": "pa-IN",
        "ta": "ta-IN",
        "te": "te-IN",
        "bn": "bn-IN",
        "mr": "mr-IN",
        "gu": "gu-IN",
        "kn": "kn-IN",
        "ml": "ml-IN",
        "ur": "ur-PK"
    }

    # Translation matrices for EOC command terms and alerts across 11 languages
    DICT = {
        "hi": { # Hindi
            "incident_summary": "🚨 घटना का सारांश",
            "threat_level": "खतरे का स्तर",
            "available_resources": "उपलब्ध संसाधन",
            "recommended_response": "अनुशंसित प्रतिक्रिया स्थिति",
            "threat_assessment": "📊 खतरे के स्तर का आकलन",
            "risk_reasoning": "जोखिम आकलन तर्क",
            "security_dashboard": "🔒 सुरक्षा स्वास्थ्य डैशबोर्ड",
            "verified_news": "📰 सत्यापित आपदा समाचार",
            "timeline": "📅 घटना की समयरेखा",
            "weather_indicators": "🌦️ वायुमंडलीय मौसम संकेतक",
            "gis_map": "🗺️ इंटरएक्टिव आपातकालीन जीआईएस मानचित्र",
            "safety_panels": "🛡️ सार्वजनिक सुरक्षा कमान पैनल",
            "recommended_plan": "📋 अनुशंसित कार्य योजना",
            "download_report": "📥 आपदा खुफिया रिपोर्ट डाउनलोड करें",
            "CRITICAL": "गंभीर",
            "HIGH": "उच्च",
            "MEDIUM": "मध्यम",
            "LOW": "निम्न",
            "police": "पुलिस",
            "ambulance": "एम्बुलेंस",
            "fire": "अग्निशमन सेवा",
            "disaster_management": "आपदा प्रबंधन",
            "specialist_authority": "विशेषज्ञ प्राधिकरण",
            "nearest_hospital": "निकटतम चिकित्सा केंद्र",
            "distance": "दूरी",
            "address": "पता",
            "evacuation_instructions": "निकासी के निर्देश",
            "immediate_actions": "तत्काल कार्रवाई",
            "what_to_avoid": "बचने योग्य बातें"
        },
        "pa": { # Punjabi
            "incident_summary": "🚨 ਘਟਨਾ ਦਾ ਸਾਰ",
            "threat_level": "ਖ਼ਤਰੇ ਦਾ ਪੱਧਰ",
            "available_resources": "ਉਪਲਬਧ ਸਰੋਤ",
            "recommended_response": "ਸਿਫਾਰਸ਼ ਕੀਤੀ ਪ੍ਰਤੀਕਿਰਿਆ ਸਥਿਤੀ",
            "threat_assessment": "📊 ਖ਼ਤਰੇ ਦੇ ਪੱਧਰ ਦਾ ਮੁਲਾਂਕਣ",
            "risk_reasoning": "ਜੋਖਮ ਮੁਲਾਂਕਣ ਤਰਕ",
            "security_dashboard": "🔒 ਸੁਰੱਖਿਆ ਸਿਹਤ ਡੈਸ਼ਬੋਰਡ",
            "verified_news": "📰 ਪ੍ਰਮਾਣਿਤ ਆਫ਼ਤ ਖ਼ਬਰਾਂ",
            "timeline": "📅 ਘਟਨਾ ਦੀ ਸਮਾਂਰੇਖਾ",
            "weather_indicators": "🌦️ ਵਾਯੂਮੰਡਲ ਮੌਸਮ ਸੂਚਕ",
            "gis_map": "🗺️ ਇੰਟਰਐਕਟਿਵ ਐਮਰਜੈਂਸੀ ਜੀਆਈਐਸ ਨਕਸ਼ਾ",
            "safety_panels": "🛡️ ਪਬਲਿਕ ਸੁਰੱਖਿਆ ਕਮਾਂਡ ਪੈਨਲ",
            "recommended_plan": "📋 ਸਿਫਾਰਸ਼ ਕੀਤੀ ਕਾਰਜ ਯੋਜਨਾ",
            "download_report": "📥 ਆਫ਼ਤ ਰਿਪੋਰਟ ਡਾਊਨਲੋਡ ਕਰੋ",
            "CRITICAL": "ਬਹੁਤ ਗੰਭੀਰ",
            "HIGH": "ਉੱਚ",
            "MEDIUM": "ਮੱਧਮ",
            "LOW": "ਘੱਟ",
            "police": "ਪੁਲਿਸ",
            "ambulance": "ਐਂਬੂਲੈਂਸ",
            "fire": "ਫਾਇਰ ਬ੍ਰਿਗੇਡ",
            "disaster_management": "ਆਫ਼ਤ ਪ੍ਰਬੰਧਨ",
            "specialist_authority": "ਮਾਹਰ ਅਥਾਰਟੀ",
            "nearest_hospital": "ਨਜ਼ਦੀਕੀ ਹਸਪਤਾਲ",
            "distance": "ਦੂਰੀ",
            "address": "ਪਤਾ",
            "evacuation_instructions": "ਖਾਲੀ ਕਰਨ ਦੇ ਨਿਰਦੇਸ਼",
            "immediate_actions": "ਤੁਰੰਤ ਕਾਰਵਾਈ",
            "what_to_avoid": "ਪਰਹੇਜ਼ ਕਰਨ ਯੋਗ ਗੱਲਾਂ"
        },
        "ta": { # Tamil
            "incident_summary": "🚨 சம்பவச் சுருக்கம்",
            "threat_level": "ஆபத்து நிலை",
            "available_resources": "கிடைக்கக்கூடிய வளங்கள்",
            "recommended_response": "பரிந்துரைக்கப்பட்ட பதில் நிலை",
            "threat_assessment": "📊 ஆபத்து நிலை மதிப்பீடு",
            "risk_reasoning": "ஆபத்து மதிப்பீட்டு যুক্তি",
            "security_dashboard": "🔒 பாதுகாப்பு சுகாதார டாஷ்போர்டு",
            "verified_news": "📰 சரிபார்க்கப்பட்ட பேரிடர் செய்திகள்",
            "timeline": "📅 சம்பவ காலவரிசை",
            "weather_indicators": "🌦️ வளிமண்டல வானிலை குறிகாட்டிகள்",
            "gis_map": "🗺️ ஊடாடும் அவசர ஜிஐஎஸ் வரைபடம்",
            "safety_panels": "🛡️ பொது பாதுகாப்பு கட்டளை பேனல்கள்",
            "recommended_plan": "📋 பரிந்துரைக்கப்பட்ட செயல் திட்டம்",
            "download_report": "📥 பேரிடர் அறிக்கையைப் பதிவிறக்குக",
            "CRITICAL": "மிகவும் ஆபத்தானது",
            "HIGH": "அதிக",
            "MEDIUM": "நடுத்தர",
            "LOW": "குறைந்த",
            "police": "காவல்துறை",
            "ambulance": "ஆம்புலன்ஸ்",
            "fire": "தீயணைப்பு சேவை",
            "disaster_management": "பேரிடர் மேலாண்மை",
            "specialist_authority": "நிபுணர் அதிகாரம்",
            "nearest_hospital": "அருகிலுள்ள மருத்துவமனை",
            "distance": "தூரம்",
            "address": "முகவரி",
            "evacuation_instructions": "வெளியேற்ற வழிமுறைகள்",
            "immediate_actions": "உடனடி நடவடிக்கைகள்",
            "what_to_avoid": "தவிர்க்க வேண்டியவை"
        },
        "te": { # Telugu
            "incident_summary": "🚨 సంఘటన సారాంశం",
            "threat_level": "ప్రమాద స్థాయి",
            "available_resources": "అందుబాటులో ఉన్న వనరులు",
            "recommended_response": "సిఫార్సు చేయబడిన ప్రతిస్పందన స్థితి",
            "threat_assessment": "📊 ప్రమాద స్థాయి అంచనా",
            "risk_reasoning": "ప్రమాద అంచనా కారణాలు",
            "security_dashboard": "🔒 భద్రతా ఆరోగ్య డాష్‌బోర్డ్",
            "verified_news": "📰 ధృవీకరించబడిన విపత్తు వార్తలు",
            "timeline": "📅 సంఘటన టైమ్‌లైన్",
            "weather_indicators": "🌦️ వాతావరణ సూచికలు",
            "gis_map": "🗺️ ఇంటరాక్టివ్ ఎమర్జెన్సీ జిఐఎస్ మ్యాప్",
            "safety_panels": "🛡️ పబ్లిక్ సేఫ్టీ కమాండ్ ప్యానెల్లు",
            "recommended_plan": "📋 సిఫార్సు చేసిన కార్యాచరణ ప్రణాళిక",
            "download_report": "📥 విపత్తు నివేదికను డౌన్‌లోడ్ చేయండి",
            "CRITICAL": "తీవ్రమైనది",
            "HIGH": "ఎక్కువ",
            "MEDIUM": "మధ్యస్థం",
            "LOW": "తక్కువ",
            "police": "పోలీస్",
            "ambulance": "అంబులెన్స్",
            "fire": "ఫైర్ సర్వీసెస్",
            "disaster_management": "విపత్తు నిర్వహణ",
            "specialist_authority": "ప్రత్యేక అధికారం",
            "nearest_hospital": "సమీప ఆసుపత్రి",
            "distance": "దూరం",
            "address": "చిరునామా",
            "evacuation_instructions": "ఖాళీ చేసే సూచనలు",
            "immediate_actions": "తక్షణ చర్యలు",
            "what_to_avoid": "నివారించవలసినవి"
        },
        "bn": { # Bengali
            "incident_summary": "🚨 ঘটনার সারাংশ",
            "threat_level": "ঝুঁকির মাত্রা",
            "available_resources": "উপলব্ধ সম্পদ",
            "recommended_response": "প্রস্তাবিত প্রতিক্রিয়া অবস্থা",
            "threat_assessment": "📊 ঝুঁকির মাত্রা মূল্যায়ন",
            "risk_reasoning": "ঝুঁকি মূল্যায়নের যুক্তি",
            "security_dashboard": "🔒 সুরক্ষা স্বাস্থ্য ড্যাশবোর্ড",
            "verified_news": "📰 যাচাইকৃত দুর্যোগ সংবাদ",
            "timeline": "📅 ঘটনার টাইমলাইন",
            "weather_indicators": "🌦️ আবহাওয়া সূচক",
            "gis_map": "🗺️ ইন্টারেক্টিভ জরুরি জিআইএস মানচিত্র",
            "safety_panels": "🛡️ জননিরাপত্তা কমান্ড প্যানেল",
            "recommended_plan": "📋 প্রস্তাবিত কর্ম পরিকল্পনা",
            "download_report": "📥 দুর্যোগ রিপোর্ট ডাউনলোড করুন",
            "CRITICAL": "চরম সংকটজনক",
            "HIGH": "উচ্চ",
            "MEDIUM": "মাঝারি",
            "LOW": "নিম্ন",
            "police": "পুলিশ",
            "ambulance": "অ্যাম্বুলেন্স",
            "fire": "দমকল বাহিনী",
            "disaster_management": "দুর্যোগ ব্যবস্থাপনা",
            "specialist_authority": "বিশেষজ্ঞ কর্তৃপক্ষ",
            "nearest_hospital": "নিকটবর্তী হাসপাতাল",
            "distance": "দূরত্ব",
            "address": "ঠিকানা",
            "evacuation_instructions": "স্থানান্তর নির্দেশাবলী",
            "immediate_actions": "অবিলম্বে করণীয়",
            "what_to_avoid": "বর্জনীয় বিষয়সমূহ"
        },
        "mr": { # Marathi
            "incident_summary": "🚨 घटनेचा सारांश",
            "threat_level": "धोक्याची पातळी",
            "available_resources": "उपलब्ध संसाधने",
            "recommended_response": "शिफारस केलेली प्रतिसाद स्थिती",
            "threat_assessment": "📊 धोक्याच्या पातळीचे मूल्यमापन",
            "risk_reasoning": "धोका मूल्यमापन तर्क",
            "security_dashboard": "🔒 सुरक्षा आरोग्य डॅशबोर्ड",
            "verified_news": "📰 सत्यापित आपत्ती बातम्या",
            "timeline": "📅 घटनेची टाइमलाईन",
            "weather_indicators": "🌦️ हवामान निर्देशक",
            "gis_map": "🗺️ परस्परसंवादी आपत्कालीन जीआयएस नकाशा",
            "safety_panels": "🛡️ सार्वजनिक सुरक्षा कमांड पॅनेल",
            "recommended_plan": "📋 शिफारस केलेली कृती योजना",
            "download_report": "📥 आपत्ती अहवाल डाउनलोड करा",
            "CRITICAL": "अतिशय गंभीर",
            "HIGH": "उच्च",
            "MEDIUM": "मध्यम",
            "LOW": "कमी",
            "police": "पोलीस",
            "ambulance": "रुग्णवाहिका",
            "fire": "अग्निशमन दल",
            "disaster_management": "आपत्ती व्यवस्थापन",
            "specialist_authority": "तज्ज्ञ प्राधिकरण",
            "nearest_hospital": "जवळचे रुग्णालय",
            "distance": "अंतर",
            "address": "पत्ता",
            "evacuation_instructions": "स्थलांतराचे आदेश",
            "immediate_actions": "तातडीची पावले",
            "what_to_avoid": "टाळण्यासारख्या गोष्टी"
        },
        "gu": { # Gujarati
            "incident_summary": "🚨 ઘટનાનો સારાંશ",
            "threat_level": "જોખમનું સ્તર",
            "available_resources": "ઉપલબ્ધ સંસાધનો",
            "recommended_response": "ભલામણ કરેલ પ્રતિભાવ સ્થિતિ",
            "threat_assessment": "📊 જોખમ સ્તરનું મૂલ્યાંકન",
            "risk_reasoning": "જોખમ મૂલ્યાંકન તર્ક",
            "security_dashboard": "🔒 સુરક્ષા આરોગ્ય ડેશબોર્ડ",
            "verified_news": "📰 ચકાસાયેલ આપત્તિ સમાચાર",
            "timeline": "📅 ઘટનાની સમયરેખા",
            "weather_indicators": "🌦️ હવામાન સંકેતો",
            "gis_map": "🗺️ ઇન્ટરેક્ટિવ ઇમરજન્સી જીઆઇએસ નકશો",
            "safety_panels": "🛡️ જાહેર સુરક્ષા કમાન્ડ પેનલ્સ",
            "recommended_plan": "📋 ભલામણ કરેલ કાર્ય યોજના",
            "download_report": "📥 આપત્તિ અહેવાલ ડાઉનલોડ કરો",
            "CRITICAL": "અતિ ગંભીર",
            "HIGH": "ઉચ્ચ",
            "MEDIUM": "મધ્યમ",
            "LOW": "ઓછું",
            "police": "પોલીસ",
            "ambulance": "એમ્બ્યુલન્સ",
            "fire": "અગ્નિશામક સેવા",
            "disaster_management": "આપત્તિ વ્યવસ્થાપન",
            "specialist_authority": "નિષ્ણાત સત્તામંડળ",
            "nearest_hospital": "નજીકની હોસ્પિટલ",
            "distance": "અંતર",
            "address": "સરનામું",
            "evacuation_instructions": "સ્થળાંતર માર્ગદર્શિકા",
            "immediate_actions": "તાત્કાલિક પગલાં",
            "what_to_avoid": "ટાળવાની બાબતો"
        },
        "kn": { # Kannada
            "incident_summary": "🚨 ಘಟನೆಯ ಸಾರಾಂಶ",
            "threat_level": "ಅಪಾಯದ ಮಟ್ಟ",
            "available_resources": "ಲಭ್ಯವಿರುವ ಸಂಪನ್ಮೂಲಗಳು",
            "recommended_response": "ಶಿಫಾರಸು ಮಾಡಿದ ಪ್ರತಿಕ್ರಿಯೆ ಸ್ಥಿತಿ",
            "threat_assessment": "📊 ಅಪಾಯದ ಮಟ್ಟದ ಮೌಲ್ಯಮಾಪನ",
            "risk_reasoning": "ಅಪಾಯದ ಮೌಲ್ಯಮಾಪನ ತರ್ಕ",
            "security_dashboard": "🔒 ಭದ್ರತಾ ಆರೋಗ್ಯ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            "verified_news": "📰 ಪರಿಶೀಲಿಸಿದ ವಿಪತ್ತು ಸುದ್ದಿಗಳು",
            "timeline": "📅 ಘಟನೆಯ ಟೈಮ್‌ಲೈನ್",
            "weather_indicators": "🌦️ ಹವಾಮಾನ ಸೂಚಕಗಳು",
            "gis_map": "🗺️ ಸಂವಾದಾತ್ಮಕ ತುರ್ತು ಜಿಐಎಸ್ ನಕ್ಷೆ",
            "safety_panels": "🛡️ ಸಾರ್ವಜನಿಕ ಸುರಕ್ಷತಾ ಕಮಾಂಡ್ ಪ್ಯಾನೆಲ್‌ಗಳು",
            "recommended_plan": "📋 ಶಿಫಾರಸು ಮಾಡಿದ ಕಾರ್ಯ ಯೋಜನೆ",
            "download_report": "📥 ವಿಪತ್ತು ವರದಿಯನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
            "CRITICAL": "ಅತಿ ತೀವ್ರ",
            "HIGH": "ಹೆಚ್ಚು",
            "MEDIUM": "ಮಧ್ಯಮ",
            "LOW": "ಕಡಿಮೆ",
            "police": "ಪೊಲೀಸ್",
            "ambulance": "ಆಂಬ್ಯುಲೆನ್ಸ್",
            "fire": "ಅಗ್ನಿಶಾಮಕ ಸೇವೆಗಳು",
            "disaster_management": "ವಿಪತ್ತು ನಿರ್ವಹಣೆ",
            "specialist_authority": "ತಜ್ಞ ಪ್ರಾಧಿಕಾರ",
            "nearest_hospital": "ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆ",
            "distance": "ದೂರ",
            "address": "ವಿಳಾಸ",
            "evacuation_instructions": "ಸ್ಥಳಾಂತರ ಸೂಚನೆಗಳು",
            "immediate_actions": "ತಕ್ಷಣದ ಕ್ರಮಗಳು",
            "what_to_avoid": "ತಪ್ಪಿಸಬೇಕಾದ ವಿಷಯಗಳು"
        },
        "ml": { # Malayalam
            "incident_summary": "🚨 സംഭവത്തിന്റെ സംഗ്രഹം",
            "threat_level": "അപകട നില",
            "available_resources": "ലഭ്യമായ വിഭവങ്ങൾ",
            "recommended_response": "ശുപാർശ ചെയ്യുന്ന പ്രതികരണ നില",
            "threat_assessment": "📊 അപകട നില വിലയിരുത്തൽ",
            "risk_reasoning": "റിസ്ക് വിലയിരുത്തൽ യുക്തി",
            "security_dashboard": "🔒 സുരക്ഷാ ആരോഗ്യ ഡാഷ്ബോർഡ്",
            "verified_news": "📰 സ്ഥിരീകരിച്ച ദുരന്ത വാർത്തകൾ",
            "timeline": "📅 സംഭവ ടൈംലൈൻ",
            "weather_indicators": "🌦️ കാലാവസ്ഥാ സൂചകങ്ങൾ",
            "gis_map": "🗺️ ഇൻക്യുസീവ് അടിയന്തര ജിഐഎസ് മാപ്പ്",
            "safety_panels": "🛡️ പൊതു സുരക്ഷാ കമാൻഡ് പാനലുകൾ",
            "recommended_plan": "📋 ശുപാർശ ചെയ്ത പ്രവർത്തന പദ്ധതി",
            "download_report": "📥 ദുരന്ത റിപ്പോർട്ട് ഡൗൺലോഡ് ചെയ്യുക",
            "CRITICAL": "അതിതീവ്രം",
            "HIGH": "ഉയർന്ന",
            "MEDIUM": "മിതമായ",
            "LOW": "കുറഞ്ഞ",
            "police": "പോലീസ്",
            "ambulance": "ആംബുലൻസ്",
            "fire": "ഫയർ സർവീസ്",
            "disaster_management": "ദുരന്ത നിവാരണം",
            "specialist_authority": "വിദഗ്ദ്ധ അതോറിറ്റി",
            "nearest_hospital": "ഏറ്റവും അടുത്തുള്ള ആശുപത്രി",
            "distance": "ദൂരം",
            "address": "വിലാസം",
            "evacuation_instructions": "ഒഴിപ്പിക്കൽ നിർദ്ദേശങ്ങൾ",
            "immediate_actions": "ഉടൻ ചെയ്യേണ്ട കാര്യങ്ങൾ",
            "what_to_avoid": "ഒഴിവാക്കേണ്ടവ"
        },
        "ur": { # Urdu
            "incident_summary": "🚨 واقعہ کا خلاصہ",
            "threat_level": "خطرہ کی سطح",
            "available_resources": "دستیاب وسائل",
            "recommended_response": "تجاویز کردہ جوابی کارروائی کی حیثیت",
            "threat_assessment": "📊 خطرہ کی سطح کا جائزہ",
            "risk_reasoning": "خطرہ کے جائزے کی وجہ",
            "security_dashboard": "🔒 حفاظتی صحت کا ڈیش بورڈ",
            "verified_news": "📰 تصدیق شدہ آفات کی خبریں",
            "timeline": "📅 واقعہ کی ٹائم لائن",
            "weather_indicators": "🌦️ ماحولیاتی موسمی اشارے",
            "gis_map": "🗺️ انٹرایکٹو ایمرجنシー جی آئی ایس نقشہ",
            "safety_panels": "🛡️ پبلک سیفٹی کمانڈ پینلز",
            "recommended_plan": "📋 تجاویز کردہ ایکشن پلان",
            "download_report": "📥 آفات کی رپورٹ ڈاؤن لوڈ کریں",
            "CRITICAL": "انتہائی شدید",
            "HIGH": "شدید",
            "MEDIUM": "درمیانہ",
            "LOW": "کم",
            "police": "پولیس",
            "ambulance": "ایम्बुलेंस",
            "fire": "فائر سروسز",
            "disaster_management": "ڈیزاسٹر مینجمنٹ",
            "specialist_authority": "ماہر اتھارٹی",
            "nearest_hospital": "قریب ترین ہسپتال",
            "distance": "فاصلہ",
            "address": "پتہ",
            "evacuation_instructions": "انخلاء کی ہدایات",
            "immediate_actions": "فوری اقدامات",
            "what_to_avoid": "پرہیز کرنے والی باتیں"
        }
    }

    # Core phrase mappings for alerts and recommendations translation
    PHRASES = {
        "hi": {
            "🔴 CRITICAL FLOOD WARNING": "🔴 गंभीर बाढ़ चेतावनी",
            "🔴 CRITICAL CYCLONE WARNING": "🔴 गंभीर चक्रवात चेतावनी",
            "🔴 CRITICAL EARTHQUAKE WARNING": "🔴 गंभीर भूकंप चेतावनी",
            "🔴 CRITICAL WILDFIRE WARNING": "🔴 गंभीर जंगल की आग चेतावनी",
            "🔴 CRITICAL LANDSLIDE WARNING": "🔴 गंभीर भूस्खलन चेतावनी",
            "🔴 CRITICAL DISASTER WARNING": "🔴 गंभीर आपदा चेतावनी",

            "🟠 HIGH FLOOD WARNING": "🟠 उच्च बाढ़ चेतावनी",
            "🟠 HIGH CYCLONE WARNING": "🟠 उच्च चक्रवात चेतावनी",
            "🟠 HIGH EARTHQUAKE WARNING": "🟠 उच्च भूकंप चेतावनी",
            "🟠 HIGH WILDFIRE WARNING": "🟠 उच्च जंगल की आग चेतावनी",
            "🟠 HIGH LANDSLIDE WARNING": "🟠 उच्च भूस्खलन चेतावनी",
            "🟠 HIGH DISASTER WARNING": "🟠 उच्च आपदा चेतावनी",

            "🟡 MODERATE FLOOD ALERT": "🟡 मध्यम बाढ़ चेतावनी",
            "🟡 MODERATE CYCLONE ALERT": "🟡 मध्यम चक्रवात चेतावनी",
            "🟡 MODERATE EARTHQUAKE ALERT": "🟡 मध्यम भूकंप चेतावनी",
            "🟡 MODERATE WILDFIRE ALERT": "🟡 मध्यम जंगल की आग चेतावनी",
            "🟡 MODERATE LANDSLIDE ALERT": "🟡 मध्यम भूस्खलन चेतावनी",
            "🟡 MODERATE DISASTER ALERT": "🟡 मध्यम आपदा चेतावनी",

            "🟢 LOW FLOOD MONITORING": "🟢 निम्न बाढ़ निगरानी",
            "🟢 LOW CYCLONE MONITORING": "🟢 निम्न चक्रवात निगरानी",
            "🟢 LOW EARTHQUAKE MONITORING": "🟢 निम्न भूकंप निगरानी",
            "🟢 LOW WILDFIRE MONITORING": "🟢 निम्न जंगल की आग निगरानी",
            "🟢 LOW LANDSLIDE MONITORING": "🟢 निम्न भूस्खलन निगरानी",
            "🟢 LOW DISASTER MONITORING": "🟢 निम्न आपदा निगरानी",

            "Severe flood conditions detected. Immediate evacuation may be required. Move to designated shelters. Avoid low-lying areas. Turn off main utility lines (gas/power).": 
                "बाढ़ की स्थिति पाई गई है। तुरंत खाली करने की आवश्यकता हो सकती है। नामित आश्रयों में जाएं। निचले इलाकों से बचें। मुख्य उपयोगिता लाइनों (गैस/बिजली) को बंद करें।",
            
            "Significant flood conditions building. Relocate vulnerable individuals to safe zones. Stay indoors and prepare emergency kits. Monitor official reports.":
                "बाढ़ की स्थिति बन रही है। संवेदनशील व्यक्तियों को सुरक्षित क्षेत्रों में स्थानांतरित करें। घर के अंदर रहें और आपातकालीन किट तैयार करें। आधिकारिक रिपोर्टों की निगरानी करें।"
        },
        "pa": {
            "🔴 CRITICAL FLOOD WARNING": "🔴 ਗੰਭੀਰ ਹੜ੍ਹ ਦੀ ਚੇਤਾਵਨੀ",
            "🔴 CRITICAL CYCLONE WARNING": "🔴 ਗੰਭੀਰ ਚੱਕਰਵਾਤ ਦੀ ਚੇਤਾਵਨੀ",
            "🔴 CRITICAL EARTHQUAKE WARNING": "🔴 ਗੰਭੀਰ ਭੂਚਾਲ ਦੀ ਚੇਤਾਵਨੀ",
            "🔴 CRITICAL WILDFIRE WARNING": "🔴 ਗੰਭੀਰ ਜੰਗਲੀ ਅੱਗ ਦੀ ਚੇਤਾਵਨੀ",
            "🔴 CRITICAL LANDSLIDE WARNING": "🔴 ਗੰਭੀਰ ਢਿੱਗਾਂ ਡਿੱਗਣ ਦੀ ਚੇਤਾਵਨੀ",
            "🔴 CRITICAL DISASTER WARNING": "🔴 ਗੰਭੀਰ ਆਫ਼ਤ ਦੀ ਚੇਤਾਵਨੀ",

            "Severe flood conditions detected. Immediate evacuation may be required. Move to designated shelters. Avoid low-lying areas. Turn off main utility lines (gas/power).":
                "ਹੜ੍ਹ ਦੀ ਗੰਭੀर ਸਥਿਤੀ ਬਣੀ ਹੋਈ ਹੈ। ਤੁਰੰਤ ਖਾਲੀ ਕਰਨ ਦੀ ਲੋੜ ਹੋ ਸਕਦੀ ਹੈ। ਨਿਰਧਾਰਤ ਆਸਰਾ ਘਰਾਂ ਵਿੱਚ ਜਾਓ। ਨੀਵੇਂ ਇਲਾਕਿਆਂ ਤੋਂ ਬਚੋ। ਮੁੱਖ ਬਿਜਲੀ ਅਤੇ ਗੈਸ ਸਪਲਾਈ ਬੰਦ ਕਰੋ।"
        }
        # Add basic translation helpers. If not in helper dictionary, return English/source phrase or translate words.
    }

    def translate_term(self, term: str, lang_code: str) -> str:
        """Helper to fetch a single EOC vocabulary word/phrase."""
        if lang_code == "en" or not lang_code:
            return term
        
        # Check vocab dictionary
        lang_dict = self.DICT.get(lang_code, {})
        if term in lang_dict:
            return lang_dict[term]
            
        # Check phrase dictionary
        lang_phrases = self.PHRASES.get(lang_code, {})
        if term in lang_phrases:
            return lang_phrases[term]

        return term

    def translate_report(self, result: dict, target_lang: str) -> dict:
        """
        Translates risk levels, alerts, action plans, contacts, 
        and safety instructions within the coordinated result payload.
        """
        if target_lang == "en" or not target_lang:
            return result

        # 1. Translate Alert
        alert = result.get("alert", {})
        if alert:
            result["alert"] = {
                "level": self.translate_term(alert.get("level", "LOW"), target_lang),
                "color": alert.get("color", "#48bb78"),
                "headline": self.translate_term(alert.get("headline", ""), target_lang),
                "message": self.translate_term(alert.get("message", ""), target_lang),
                "risk_score": alert.get("risk_score", 0.0)
            }

        # 2. Translate Risk
        risk = result.get("risk", {})
        if risk:
            result["risk"] = {
                "risk_score": risk.get("risk_score", 0.0),
                "severity": self.translate_term(risk.get("severity", "LOW"), target_lang),
                "reasoning": self.translate_term(risk.get("reasoning", ""), target_lang)
            }

        # 3. Translate Emergency Contacts
        contacts = result.get("emergency_contacts", {})
        if contacts:
            hosp = contacts.get("nearest_hospital", {})
            translated_hosp = {}
            if hosp:
                translated_hosp = {
                    "name": self.translate_term(hosp.get("name", ""), target_lang),
                    "distance_km": hosp.get("distance_km", 0.0),
                    "address": self.translate_term(hosp.get("address", ""), target_lang),
                    "lat": hosp.get("lat"),
                    "lon": hosp.get("lon")
                }
            result["emergency_contacts"] = {
                "police": contacts.get("police", "112"),
                "ambulance": contacts.get("ambulance", "102"),
                "fire": contacts.get("fire", "101"),
                "disaster_management": self.translate_term(contacts.get("disaster_management", ""), target_lang),
                "specialist_authority": self.translate_term(contacts.get("specialist_authority", ""), target_lang),
                "nearest_hospital": translated_hosp
            }

        # 4. Translate Safety Guidance
        guidance = result.get("safety_guidance", {})
        if guidance:
            actions = [self.translate_term(a, target_lang) for a in guidance.get("immediate_actions", [])]
            evac = [self.translate_term(e, target_lang) for e in guidance.get("evacuation_instructions", [])]
            avoid = [self.translate_term(av, target_lang) for av in guidance.get("what_to_avoid", [])]
            result["safety_guidance"] = {
                "type": self.translate_term(guidance.get("type", ""), target_lang),
                "immediate_actions": actions,
                "evacuation_instructions": evac,
                "what_to_avoid": avoid
            }

        # 5. Translate Recommended Action Plans
        plan = result.get("plan", [])
        if plan:
            result["plan"] = [self.translate_term(p, target_lang) for p in plan]

        return result
