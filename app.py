# --- BAZA SCENARIUSZY (5 WARIANTÓW) ---
ALL_SCENARIOS = {
    "Wariant A: Ransomware i paraliż HIS (3 Rundy)": {
        # ... (poprzedni kod Wariantu A - pozostaw bez zmian, lub skopiuj z poprzedniej wersji)
    },
    "Wariant B: Atak na urządzenia medyczne IoT (3 Rundy)": {
         # ... (poprzedni kod Wariantu B - pozostaw bez zmian, lub skopiuj z poprzedniej wersji)
    },
    "Wariant C: Zaawansowany Atak APT (5 Rund)": {
         # ... (poprzedni kod Wariantu C - pozostaw bez zmian, lub skopiuj z poprzedniej wersji)
    },
    
    "Wariant D: Niewidzialny Zabójca (Zatrucie Danych - 4 Rundy)": {
        1: {
            "title": "Runda 1: Podejrzany błąd w systemie (Wtorek, 11:00)",
            "desc": "Pielęgniarka na oddziale chirurgii w ostatniej chwili wstrzymuje przetoczenie krwi. Zauważa, że system HIS pokazuje grupę krwi O- dla pacjenta, którego papierowa opaska i stary wypis wskazują na AB+. Chwilę później na internie pacjent dostaje wstrząsu anafilaktycznego – z systemu 'zniknęła' informacja o jego śmiertelnej alergii na penicylinę. Systemy działają płynnie, ale dane wydają się zmienione.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Administracja Baz Danych:",
                    "options": {
                        "Natychmiastowe zablokowanie możliwości zapisu/edycji w bazie (Read-Only) i audyt logów": {"pat": +10, "avl": -10, "fin": -5, "comp": +10},
                        "Traktowanie tego jako 'błędu interfejsu' i restart serwera aplikacyjnego": {"pat": -20, "avl": +5, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna (Procedury bezpieczeństwa):",
                    "options": {
                        "Wstrzymanie wszystkich planowych operacji i transfuzji do czasu ręcznej weryfikacji grup krwi w laboratorium": {"pat": +25, "avl": 0, "fin": -15, "comp": +10},
                        "Kontynuowanie zabiegów z poleceniem 'podwójnego sprawdzania' danych przez personel na ekranach": {"pat": -30, "avl": 0, "fin": +5, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Poufne zgłoszenie incydentu na Policję (podejrzenie sabotażu wewnętrznego / Insider Threat)": {"pat": 0, "avl": 0, "fin": 0, "comp": +20},
                        "Wstrzymanie się ze zgłoszeniami do czasu 'wewnętrznego wyjaśnienia sprawy'": {"pat": 0, "avl": 0, "fin": +5, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Epidemia nieufności (Wtorek, 16:00)",
            "desc": "Audyt IT potwierdza najgorsze: ktoś z uprawnieniami administratora modyfikował wyniki badań laboratoryjnych, dawki leków onkologicznych i alergie w setkach kart pacjentów. Personel medyczny jest przerażony – lekarze odmawiają podawania leków, bo nie wiedzą, czy dawka na ekranie nie jest śmiertelna. Haker wysyła maila: 'Zatruliśmy wasze dane. Zapłaćcie 1 mln zł za listę zmienionych rekordów'.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT (Odzyskiwanie Integralności):",
                    "options": {
                        "Przywrócenie bazy danych z backupu sprzed 48 godzin (utrata wszystkich wpisów z ostatnich 2 dni)": {"pat": +10, "avl": -20, "fin": -10, "comp": +15},
                        "Próba wyśledzenia i ręcznego cofnięcia tylko złośliwych zmian na żywym organizmie (ryzyko przeoczenia)": {"pat": -25, "avl": +10, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Kliniczna:",
                    "options": {
                        "Masowe, ponowne pobieranie krwi i wywiady od wszystkich pacjentów na oddziałach (gigantyczne koszty i czas)": {"pat": +25, "avl": -10, "fin": -25, "comp": +10},
                        "Poleganie na wydrukach papierowych leżących na biurkach pielęgniarek": {"pat": -10, "avl": +5, "fin": +5, "comp": -10},
                    }
                },
                "Dir": {
                    "label": "Decyzja PR / Zarząd:",
                    "options": {
                        "Zatajenie faktu manipulacji przed pacjentami, powołanie się w mediach na 'awarię techniczną'": {"pat": -10, "avl": 0, "fin": +10, "comp": -40},
                        "Transparentne przyznanie się do ingerencji w dane, powiadomienie MZ i pacjentów o ryzyku": {"pat": +10, "avl": 0, "fin": -25, "comp": +30},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Kret czy przejęte konto? (Środa, 10:00)",
            "desc": "Służby informują, że ataku dokonano z użyciem poświadczeń (loginu i hasła) jednego z ordynatorów, który w tym czasie był na urlopie. Został ofiarą phishingu i nie miał włączonego uwierzytelniania dwuskładnikowego (2FA/MFA). Dziennikarze śledczy ujawniają sprawę, nagłówki krzyczą: 'Zabójcze dawki w szpitalu'.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Zarządzanie Tożsamością:",
                    "options": {
                        "Wymuszone, natychmiastowe wdrożenie MFA (kody SMS/Aplikacja) dla wszystkich, mimo oporu personelu medycznego": {"pat": +10, "avl": -15, "fin": -10, "comp": +25},
                        "Tylko zresetowanie wszystkich haseł w szpitalu na 'silniejsze' (szybsze do wdrożenia)": {"pat": -15, "avl": +10, "fin": +5, "comp": -15},
                    }
                },
                "Med": {
                    "label": "Decyzja Lekarska (Zarządzanie Zespołem):",
                    "options": {
                        "Wysłanie całego personelu na pilne, 2-godzinne szkolenie z cyber-higieny, kosztem opóźnień na izbie przyjęć": {"pat": +15, "avl": -10, "fin": -10, "comp": +15},
                        "Pozostawienie lekarzy przy pacjentach, przesłanie instrukcji bezpieczeństwa jedynie mailem": {"pat": -10, "avl": +15, "fin": +5, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Prawno-Kadrowa:",
                    "options": {
                        "Ochrona zmanipulowanego ordynatora (był ofiarą), skupienie się na naprawie procesów w IT": {"pat": 0, "avl": 0, "fin": 0, "comp": +15},
                        "Publiczne zwolnienie ordynatora dyscyplinarnie i zrzucenie na niego całej winy za wyciek haseł": {"pat": -5, "avl": 0, "fin": +10, "comp": -15},
                    }
                }
            }
        },
        4: {
            "title": "Runda 4: Rozliczenie z zaufania (Czwartek, 12:00)",
            "desc": "Kryzys został opanowany. Udało się odtworzyć prawidłowe dane z backupów i ponownych badań. Szpital jednak stoi przed ogromnymi pozwami zbiorowymi od pacjentów, którzy dowiedzieli się, że podano im (lub omal nie podano) złe leki. KNF i MZ analizują wasze decyzje.",
            "questions": {
                "IT": {
                    "label": "Nowa Polityka IT:",
                    "options": {
                        "Wdrożenie systemu klasy DLP (Data Loss Prevention) i zaawansowanego monitorowania logów dostępu (duży koszt operacyjny)": {"pat": +15, "avl": +5, "fin": -25, "comp": +20},
                        "Brak zmian strukturalnych, uznanie incydentu za 'nieszczęśliwy, jednorazowy wypadek'": {"pat": -20, "avl": +10, "fin": +15, "comp": -30},
                    }
                },
                "Med": {
                    "label": "Relacje z Pacjentami:",
                    "options": {
                        "Uruchomienie darmowych badań kontrolnych dla wszystkich pacjentów, których dane były w modyfikowanej puli": {"pat": +25, "avl": -5, "fin": -30, "comp": +15},
                        "Oczekiwanie na indywidualne pozwy, brak proaktywnych działań rekompensacyjnych": {"pat": -10, "avl": +5, "fin": +10, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Strategiczna Dyrekcji:",
                    "options": {
                        "Powołanie stanowiska oficera ds. integralności danych klinicznych": {"pat": +10, "avl": 0, "fin": -10, "comp": +15},
                        "Przeznaczenie budżetu naprawczego wyłącznie na kampanię PR-ową 'Oczyszczanie wizerunku'": {"pat": -10, "avl": 0, "fin": -15, "comp": -20},
                    }
                }
            }
        }
    },
    
    "Wariant E: Przerwany Łańcuch (Atak na Telemedycynę - 4 Rundy)": {
        1: {
            "title": "Runda 1: Paraliż zewnętrzny (Środa, 18:00)",
            "desc": "Zewnętrzna, komercyjna chmura, do której szpital wysyła nocą zdjęcia TK i MR do opisu (zewnętrzni radiolodzy), nagle przestaje odpowiadać. Równolegle, platforma do monitorowania pacjentów kardiologicznych w domach (Holtery online) zgłasza błąd API. To wasi główni dostawcy (Third-Party).",
            "questions": {
                "IT": {
                    "label": "Decyzja IT (Reakcja na awarię chmury):",
                    "options": {
                        "Natychmiastowe zerwanie tunelu VPN (API) łączącego szpital z chmurą dostawcy (Prewencyjny Air-Gap)": {"pat": 0, "avl": -20, "fin": -5, "comp": +15},
                        "Czekanie na odpowiedź supportu dostawcy. Utrzymywanie otwartych połączeń API": {"pat": -15, "avl": +5, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Kliniczna (Radiologia):",
                    "options": {
                        "Wezwanie lokalnych radiologów na nadgodziny do szpitala, by opisywali zdjęcia na miejscu (Ogromne koszty)": {"pat": +20, "avl": +10, "fin": -25, "comp": +5},
                        "Wstrzymanie opisów zdjęć planowych do czasu powrotu chmury, diagnozowanie tylko przypadków 'na ratunek życia'": {"pat": -15, "avl": -10, "fin": +10, "comp": -5},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji (Zarządzanie Kryzysowe):",
                    "options": {
                        "Aktywacja planu BCP: wdrożenie papierowych procedur dla pacjentów z telemonitoringu": {"pat": +15, "avl": 0, "fin": -10, "comp": +10},
                        "Brak aktywacji BCP, to 'tylko awaria po stronie dostawcy'": {"pat": -20, "avl": 0, "fin": +5, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Zaraza po łączach (Środa, 22:00)",
            "desc": "Dostawca chmurowy wydaje komunikat: padli ofiarą zaawansowanego Ransomware typu 'Worm'. Wirus replikuje się przez aktywne połączenia API. Jeśli nie zerwaliście z nimi połączenia w Rundzie 1, wirus właśnie puka do waszych wewnętrznych serwerów. Co gorsza, dostawca przyznaje, że wyciekły dane telemetryczne pacjentów kardiologicznych z waszego szpitala.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT (Obrona perymetru):",
                    "options": {
                        "Radykalne odcięcie całego szpitala od sieci Internet na 24h, aby skanować sieć wewnętrzną pod kątem wirusa z chmury": {"pat": -10, "avl": -30, "fin": -15, "comp": +25},
                        "Pozostawienie szpitala w sieci, aktualizacja sygnatur antywirusowych i blokowanie tylko adresów IP dostawcy": {"pat": -25, "avl": +15, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Kliniczna (Kardiologia):",
                    "options": {
                        "Rozesłanie karetek i wezwanie najciężej chorych z telemonitoringu na fizyczną obserwację na oddział": {"pat": +30, "avl": 0, "fin": -30, "comp": +10},
                        "Wysłanie SMS-ów do pacjentów z prośbą o 'zgłoszenie się w razie złego samopoczucia'": {"pat": -30, "avl": 0, "fin": +10, "comp": -15},
                    }
                },
                "Dir": {
                    "label": "Decyzja prawna i RODO:",
                    "options": {
                        "Zgłoszenie do UODO wycieku po stronie dostawcy, biorąc na siebie obowiązek poinformowania pacjentów (jako administrator danych)": {"pat": +10, "avl": 0, "fin": -5, "comp": +30},
                        "Próba przerzucenia całkowitej odpowiedzialności prawnej na dostawcę, brak zgłoszeń do UODO z ramienia szpitala": {"pat": 0, "avl": 0, "fin": 0, "comp": -35},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Odpowiedzialność Stron Trzecich (Czwartek, 08:00)",
            "desc": "Pacjenci są przerażeni, że ktoś obcy ma ich dane medyczne z rozruszników serca. W lokalnych mediach pojawiają się artykuły oskarżające szpital o 'oszczędzanie na bezpieczeństwie' poprzez tanich dostawców IT. Szpital jest całkowicie pozbawiony zdalnej radiologii, kolejki na SOR rosną wykładniczo.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT (Strategia Odbudowy):",
                    "options": {
                        "Wymuszenie na nowym dostawcy rygorystycznego audytu bezpieczeństwa i testów penetracyjnych (TLPT) przed podpisaniem umowy": {"pat": +10, "avl": -10, "fin": -15, "comp": +25},
                        "Podpisanie umowy z najtańszym zastępczym dostawcą chmury bez audytów, aby szybko udrożnić opisy RTG": {"pat": -20, "avl": +25, "fin": +15, "comp": -30},
                    }
                },
                "Med": {
                    "label": "Decyzja Komunikacyjna (Lekarz-Pacjent):",
                    "options": {
                        "Osobiste telefony od lekarzy prowadzących do zaniepokojonych pacjentów kardiologicznych (ogromny wysiłek kadrowy)": {"pat": +25, "avl": -5, "fin": -15, "comp": +15},
                        "Wydanie bezosobowego oświadczenia na stronie internetowej szpitala": {"pat": -15, "avl": 0, "fin": +5, "comp": -15},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji (NIS2):",
                    "options": {
                        "Rozwiązanie umowy z winnym dostawcą i pozew sądowy o utracone korzyści i straty wizerunkowe": {"pat": +5, "avl": 0, "fin": +10, "comp": +15},
                        "Utrzymanie dostawcy, ale wynegocjowanie 'darmowego roku' w ramach rekompensaty (akceptacja wysokiego ryzyka powtórki)": {"pat": -25, "avl": +10, "fin": +25, "comp": -25},
                    }
                }
            }
        },
        4: {
            "title": "Runda 4: Architektura Przyszłości (Piątek)",
            "desc": "Systemy powoli wracają do normy, ale Ministerstwo Zdrowia domaga się pilnego raportu z zarządzania ryzykiem łańcucha dostaw (Supply Chain Risk). Zdarzenie uwidoczniło, jak bardzo szpital był uzależniony od jednej zewnętrznej platformy.",
            "questions": {
                "IT": {
                    "label": "Nowa Architektura IT:",
                    "options": {
                        "Rozproszenie ryzyka: wdrożenie strategii wielu dostawców (Multi-Cloud) z automatycznym zapasem (Failover)": {"pat": +15, "avl": +20, "fin": -35, "comp": +20},
                        "Powrót do lokalnych, własnych serwerów w piwnicy szpitala (odrzucenie innowacji telemedycznych ze strachu)": {"pat": -10, "avl": -15, "fin": -10, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Polityka Medyczna:",
                    "options": {
                        "Wprowadzenie rygorystycznych, papierowych i fizycznych planów awaryjnych dla każdej nowej cyfrowej technologii medycznej": {"pat": +20, "avl": 0, "fin": -10, "comp": +20},
                        "Poleganie całkowicie na technologii, redukcja klasycznego sprzętu diagnostycznego w celu cięcia kosztów": {"pat": -25, "avl": +10, "fin": +20, "comp": -25},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Powołanie Działu Zarządzania Ryzykiem Stron Trzecich (wymóg NIS2/DORA) monitorującego wszystkich vendorów": {"pat": +15, "avl": 0, "fin": -15, "comp": +25},
                        "Pozostawienie weryfikacji dostawców w rękach Działu Zakupów (skupionego tylko na niskiej cenie)": {"pat": -20, "avl": 0, "fin": +15, "comp": -30},
                    }
                }
            }
        }
    }
}