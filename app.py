import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cyberatak na Szpital - Symulacja", layout="wide", page_icon="🏥")

# --- STAN GRY ---
@st.cache_resource
def get_game_state():
    return {
        "round": 0, 
        "teams": {}, 
        "active_scenario": "Wariant A: Ransomware i paraliż HIS (3 Rundy)" 
    }

state = get_game_state()

# --- BAZA SCENARIUSZY (5 WARIANTÓW) ---
ALL_SCENARIOS = {
    "Wariant A: Ransomware i paraliż HIS (3 Rundy)": {
        1: {
            "title": "Runda 1: Pierwsze symptomy infekcji",
            "desc": "Godzina 14:00. Lekarze na Szpitalnym Oddziale Ratunkowym (SOR) zgłaszają, że system HIS (Hospital Information System) działa bardzo wolno. Na kilku komputerach w rejestracji pojawiły się dziwne, czarne ekrany. Pacjenci w kolejce zaczynają się denerwować.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Cyberbezpieczeństwo:",
                    "options": {
                        "Natychmiastowe odcięcie SOR od głównej sieci (Downtime prewencyjny)": {"pat": 0, "avl": -20, "fin": -5, "comp": +10},
                        "Analiza logów w tle i próba zdalnego restartu stacji w rejestracji": {"pat": -10, "avl": +5, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Wdrożenie procedury 'Downtime': przejście na papierową dokumentację": {"pat": +15, "avl": 0, "fin": -5, "comp": +10},
                        "Wstrzymanie wypisów i przyjęć planowych do czasu powrotu systemu": {"pat": -15, "avl": 0, "fin": -15, "comp": -5},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Powiadomienie Centrum e-Zdrowia (CeZ) o potencjalnych problemach": {"pat": 0, "avl": 0, "fin": 0, "comp": +15},
                        "Brak eskalacji na zewnątrz, czekamy na diagnozę wewnętrzną IT": {"pat": 0, "avl": 0, "fin": 0, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Żądanie Okupu i Stan Wyjątkowy",
            "desc": "Godzina 16:30. Diagnoza jest najgorsza z możliwych: Ransomware zaszyfrował bazy danych pacjentów. Na ekranach wyświetla się żądanie 50 Bitcoinów. Laboratorium nie może przesyłać wyników, a lekarze nie znają dawek leków dla pacjentów na oddziałach.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Cyberbezpieczeństwo:",
                    "options": {
                        "Twardy reset i wyłączenie głównych serwerów, wezwanie CERT Polska": {"pat": -10, "avl": -30, "fin": -10, "comp": +25},
                        "Próba odzyskania danych z porannych kopii bez wyłączania sieci": {"pat": -25, "avl": -10, "fin": -20, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Przekierowanie karetek do innych szpitali, wypisywanie pacjentów stabilnych": {"pat": +20, "avl": 0, "fin": -20, "comp": +10},
                        "Próba kontynuacji leczenia wszystkich pacjentów 'na ślepo'": {"pat": -40, "avl": 0, "fin": 0, "comp": -30},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Odmowa negocjacji z hakerami, powołanie sztabu kryzysowego z Policją": {"pat": 0, "avl": 0, "fin": +10, "comp": +20},
                        "Nawiązanie tajnego kontaktu z hakerami, próba negocjacji okupu": {"pat": -10, "avl": 0, "fin": -40, "comp": -25},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Rekonwalescencja i Audyt",
            "desc": "Dzień 3. Trwa mozolne odtwarzanie systemów. Pod placówką stoją wozy transmisyjne, a do drzwi puka kontrola z Urzędu Ochrony Danych Osobowych (UODO) pytając o wyciek danych wrażliwych.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Architektura:",
                    "options": {
                        "Odbudowa sieci od zera z pełną mikrosegmentacją (potrwa tygodnie)": {"pat": +10, "avl": -15, "fin": -20, "comp": +20},
                        "Szybkie załatanie dziur i przywrócenie starej architektury": {"pat": -20, "avl": +20, "fin": +10, "comp": -25},
                    }
                },
                "Med": {
                    "label": "Decyzja PR:",
                    "options": {
                        "Otwarty komunikat o naruszeniu danych, uruchomienie infolinii": {"pat": +10, "avl": 0, "fin": -10, "comp": +25},
                        "Zasłanianie się tajemnicą śledztwa, odmawianie komentarzy": {"pat": -10, "avl": 0, "fin": -20, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Szkolenia antyphishingowe dla 100% personelu przed dopuszczeniem do systemów": {"pat": +15, "avl": -5, "fin": -10, "comp": +15},
                        "Ignorowanie szkoleń, zrzucenie winy wyłącznie na program antywirusowy": {"pat": -15, "avl": 0, "fin": 0, "comp": -20},
                    }
                }
            }
        }
    },
    
    "Wariant B: Atak na urządzenia medyczne IoT (3 Rundy)": {
        1: {
            "title": "Runda 1: Utrata synchronizacji aparatury",
            "desc": "Godzina 03:00 w nocy. Oddział Intensywnej Terapii Medycznej (OiTM). Kardiomonitory nagle tracą łączność z centralą na biurku pielęgniarek. Dwie pompy infuzyjne (podłączone do Wi-Fi) zaczynają emitować fałszywe alarmy krytyczne.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / SOC:",
                    "options": {
                        "Natychmiastowe odcięcie sieci Wi-Fi dla urządzeń medycznych (IoT)": {"pat": +10, "avl": -20, "fin": -5, "comp": +5},
                        "Zdalny restart centrali monitorującej (utrzymanie sieci w działaniu)": {"pat": -15, "avl": +10, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Przejście na manualne, fizyczne monitorowanie pacjentów (wymaga 100% obłożenia)": {"pat": +25, "avl": 0, "fin": -10, "comp": +10},
                        "Zignorowanie anomalii jako 'kolejnej awarii sprzętu'": {"pat": -40, "avl": 0, "fin": 0, "comp": -30},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Skierowanie dodatkowego personelu medycznego z innych oddziałów na OiTM": {"pat": +20, "avl": 0, "fin": -15, "comp": 0},
                        "Czekanie na raport z porannej zmiany": {"pat": -20, "avl": 0, "fin": 0, "comp": -10},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Szantaż na życiu pacjentów",
            "desc": "Godzina 05:00. Hakerzy udowadniają, że mają dostęp do interfejsów pomp infuzyjnych i grożą zdalną zmianą dawek leków ratujących życie, jeśli szpital nie zapłaci okupu w ciągu 2 godzin.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / Cyberbezpieczeństwo:",
                    "options": {
                        "Fizyczne wyciągnięcie kabli zasilających routery na OiTM (tzw. air-gap)": {"pat": +20, "avl": -30, "fin": -5, "comp": +15},
                        "Próba znalezienia złośliwego oprogramowania w sieci online": {"pat": -30, "avl": -5, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Odłączenie chorych od pomp i podawanie leków metodami grawitacyjnymi": {"pat": +25, "avl": -10, "fin": -5, "comp": +10},
                        "Ewakuacja całego oddziału OiTM do innego szpitala na sygnale": {"pat": -15, "avl": -20, "fin": -30, "comp": +5},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Zgłoszenie incydentu krytycznego do CSIRT GOV w trybie pilnym": {"pat": 0, "avl": 0, "fin": 0, "comp": +30},
                        "Zatajenie ataku. Próba samodzielnej negocjacji dla ratowania pacjentów": {"pat": -10, "avl": 0, "fin": -30, "comp": -40},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Dochodzenie po incydencie",
            "desc": "Dzień następny. Sieć zabezpieczona. Luki pochodziły z niezaktualizowanego oprogramowania pomp zakupionych 8 lat temu. NFZ grozi wstrzymaniem finansowania oddziału.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Wydzielenie osobnej, hermetycznej sieci VLAN dla urządzeń medycznych (IoMT)": {"pat": +15, "avl": +10, "fin": -15, "comp": +20},
                        "Podłączenie sprzętu z powrotem do ogólnej sieci po zmianie haseł": {"pat": -25, "avl": +20, "fin": +5, "comp": -30},
                    }
                },
                "Med": {
                    "label": "Decyzja PR:",
                    "options": {
                        "Zawieszenie przyjmowania ostrego dyżuru i szczera komunikacja o audycie sprzętu": {"pat": +10, "avl": -15, "fin": -15, "comp": +10},
                        "Komunikowanie 'chwilowych usterek technicznych', kontynuacja przyjęć": {"pat": -15, "avl": +10, "fin": +10, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Rozpoczęcie programu wymiany przestarzałego sprzętu medycznego (potężne koszty)": {"pat": +25, "avl": +10, "fin": -40, "comp": +20},
                        "Pozwanie producenta pomp o wadliwe oprogramowanie": {"pat": -5, "avl": 0, "fin": +15, "comp": 0},
                    }
                }
            }
        }
    },
    
    "Wariant C: Zaawansowany Atak APT (5 Rund)": {
        1: {
            "title": "Runda 1: Niewinne anomalia czy zwiad? (Piątek, 09:00)",
            "desc": "Zaczyna się niewinnie. Helpdesk odnotowuje o 30% więcej zgłoszeń od lekarzy, którzy skarżą się na powolne wczytywanie zdjęć rentgenowskich z systemu PACS. Równolegle, system pocztowy w administracji na chwilę odrzuca hasła kilkunastu pracowników.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT / SOC:",
                    "options": {
                        "Izolujemy serwer laboratoryjny i resetujemy hasła w administracji (Utrudnienia w pracy)": {"pat": 0, "avl": -10, "fin": -5, "comp": +10},
                        "Włączamy tryb głębokiego monitorowania sieci, ale nie przerywamy pracy": {"pat": -5, "avl": +5, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Wydanie zalecenia dla diagnostów o ręcznym opisywaniu pilnych zdjęć RTG": {"pat": +10, "avl": 0, "fin": -5, "comp": 0},
                        "Oczekiwanie na ustabilizowanie się systemu PACS, standardowy tryb pracy": {"pat": -10, "avl": 0, "fin": 0, "comp": 0},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Zwołanie wstępnego, niejawnego sztabu kryzysowego z udziałem zarządu i szefa IT": {"pat": +5, "avl": 0, "fin": -5, "comp": +5},
                        "Uznanie sytuacji za standardową awarię IT, brak działań zarządczych": {"pat": -10, "avl": 0, "fin": +5, "comp": -5},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Uderzenie i Lateral Movement (Piątek, 21:00)",
            "desc": "O 21:00 ekrany na stanowiskach pielęgniarek robią się czarne, pojawia się żądanie 2 milionów złotych. Co gorsza, hakerzy przejęli system zarządzania budynkiem (BMS). Klimatyzacja na trzech czynnych blokach operacyjnych zaczyna wariować – temperatura drastycznie spada.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Odcięcie głównego zasilania serwerowni i sieci logicznej (Twardy Blackout)": {"pat": -10, "avl": -40, "fin": -15, "comp": +20},
                        "Próba odzyskania kontroli nad systemem BMS bez wyłączania sieci": {"pat": -30, "avl": -10, "fin": -10, "comp": -15},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna (Bloki Operacyjne):",
                    "options": {
                        "Przyspieszone zamykanie operacji, ewakuacja bloków, wentylacja ręczna (AMBU)": {"pat": +25, "avl": 0, "fin": -10, "comp": +10},
                        "Kontynuowanie operacji za wszelką cenę mimo niestabilnego środowiska": {"pat": -40, "avl": 0, "fin": -20, "comp": -30},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Zgłoszenie 'Zdarzenia Masowego' do wojewody, przekierowanie karetek": {"pat": +20, "avl": 0, "fin": -25, "comp": +20},
                        "Próba wewnętrznego opanowania sytuacji, zakaz informowania mediów": {"pat": -20, "avl": 0, "fin": +10, "comp": -35},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Szantaż Medialny i Panika (Sobota, 10:00)",
            "desc": "Systemy wciąż leżą. Hakerzy, widząc, że szpital nie płaci, publikują fragment dokumentacji medycznej lokalnego polityka. Pod szpitalem zbierają się zaniepokojone rodziny pacjentów domagające się informacji o bliskich. Infolinia jest zablokowana.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Zaangażowanie zewnętrznej, profesjonalnej firmy Incident Response (duże koszty)": {"pat": +10, "avl": +15, "fin": -30, "comp": +20},
                        "Odtwarzanie systemów własnymi siłami przez wycieńczonych, lokalnych informatyków": {"pat": -10, "avl": -10, "fin": +15, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja PR / Obsługa Rodzin:",
                    "options": {
                        "Wysłanie lekarzy i psychologów przed budynek, szczere rozmowy z rodzinami": {"pat": +15, "avl": 0, "fin": -5, "comp": +10},
                        "Zasłanianie się ochroną budynku, odmawianie dostępu komukolwiek": {"pat": -15, "avl": 0, "fin": 0, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Zorganizowanie konferencji prasowej: przyznanie się do wycieku RODO": {"pat": +5, "avl": 0, "fin": -15, "comp": +25},
                        "Zablokowanie wypowiedzi dla mediów, straszenie dziennikarzy pozwami": {"pat": -5, "avl": 0, "fin": +5, "comp": -30},
                    }
                }
            }
        },
        4: {
            "title": "Runda 4: Paraliż Kliniczny i Interwencja Nadzoru (Niedziela, 14:00)",
            "desc": "Personel medyczny jest na skraju wyczerpania pracą na papierze. Lekarze muszą podawać leki onkologiczne 'z pamięci', co jest skrajnie niebezpieczne. Do szpitala wkraczają kontrolerzy z MZ i UODO.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT (Śledztwo vs. Odbudowa):",
                    "options": {
                        "Wstrzymanie odtwarzania i przekazanie serwerów organom śledczym jako dowód": {"pat": -15, "avl": -20, "fin": 0, "comp": +30},
                        "Priorytetyzacja przywrócenia bazy leków, odmawiając oddania serwerów natychmiast": {"pat": +25, "avl": +20, "fin": -10, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Kliniczna (Triage kryzysowy):",
                    "options": {
                        "Powołanie Komisji Etycznej do decydowania o podawaniu leków ratujących życie": {"pat": +15, "avl": 0, "fin": 0, "comp": +10},
                        "Podawanie leków metodą 'kto pierwszy ten lepszy', unikanie odpowiedzialności": {"pat": -30, "avl": 0, "fin": 0, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Pełna współpraca z MZ i UODO, udostępnienie całości dokumentacji": {"pat": 0, "avl": 0, "fin": 0, "comp": +25},
                        "Wpuszczenie nadzoru tylko z prawnikami, ukrywanie wcześniejszych zaniedbań": {"pat": 0, "avl": 0, "fin": -20, "comp": -30},
                    }
                }
            }
        },
        5: {
            "title": "Runda 5: Post-Mortem i Rozliczenie (Dzień 7)",
            "desc": "Systemy zostały częściowo przywrócone. Straty wizerunkowe są olbrzymie, planowane zabiegi opóźnione. KNF, MZ i UODO przygotowują raport końcowy. Czas na strategiczne decyzje.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT (Nowa Architektura):",
                    "options": {
                        "Migracja krytycznych systemów do bezpiecznej Chmury z architekturą Zero Trust": {"pat": +10, "avl": +30, "fin": -30, "comp": +20},
                        "Odbudowa lokalnej serwerowni w piwnicy szpitala i zakup 'lepszego antywirusa'": {"pat": -10, "avl": -15, "fin": +15, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Szkolenia Personelu:",
                    "options": {
                        "Obowiązkowe, comiesięczne symulacje ataków (Downtime Drills) dla lekarzy": {"pat": +20, "avl": 0, "fin": -10, "comp": +15},
                        "Jednorazowe szkolenie e-learningowe dla personelu": {"pat": -15, "avl": 0, "fin": +5, "comp": -15},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Dyrektor składa dymisję, biorąc odpowiedzialność za luki": {"pat": 0, "avl": 0, "fin": +20, "comp": +10},
                        "Dyrektor zwalnia Głównego Informatyka i zatrudnia kogoś z zewnątrz": {"pat": 0, "avl": 0, "fin": -10, "comp": -10},
                    }
                }
            }
        }
    },

    "Wariant D: Niewidzialny Zabójca (Zatrucie Danych - 4 Rundy)": {
        1: {
            "title": "Runda 1: Podejrzany błąd w systemie (Wtorek, 11:00)",
            "desc": "Pielęgniarka wstrzymuje przetoczenie krwi. Zauważa, że system HIS pokazuje grupę krwi O- dla pacjenta, którego opaska wskazuje na AB+. Chwilę później pacjent dostaje wstrząsu – z systemu 'zniknęła' informacja o jego śmiertelnej alergii. Systemy działają płynnie, ale dane wydają się zmienione.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Natychmiastowe zablokowanie zapisu w bazie (Read-Only) i audyt logów": {"pat": +10, "avl": -10, "fin": -5, "comp": +10},
                        "Traktowanie tego jako 'błędu interfejsu' i restart serwera aplikacyjnego": {"pat": -20, "avl": +5, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Wstrzymanie planowych operacji do czasu ręcznej weryfikacji grup krwi w laboratorium": {"pat": +25, "avl": 0, "fin": -15, "comp": +10},
                        "Kontynuowanie zabiegów z poleceniem 'podwójnego sprawdzania' danych": {"pat": -30, "avl": 0, "fin": +5, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Poufne zgłoszenie incydentu na Policję (podejrzenie sabotażu wewnętrznego)": {"pat": 0, "avl": 0, "fin": 0, "comp": +20},
                        "Wstrzymanie się ze zgłoszeniami do czasu 'wewnętrznego wyjaśnienia sprawy'": {"pat": 0, "avl": 0, "fin": +5, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Epidemia nieufności (Wtorek, 16:00)",
            "desc": "Audyt IT potwierdza najgorsze: ktoś z uprawnieniami administratora modyfikował wyniki badań, dawki leków i alergie. Lekarze odmawiają podawania leków, bo nie wiedzą, czy dawka na ekranie nie jest śmiertelna. Haker wysyła maila z żądaniem okupu za listę zmienionych rekordów.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Przywrócenie bazy danych z backupu sprzed 48 godzin (utrata wpisów z 2 dni)": {"pat": +10, "avl": -20, "fin": -10, "comp": +15},
                        "Próba wyśledzenia i ręcznego cofnięcia tylko złośliwych zmian na żywym organizmie": {"pat": -25, "avl": +10, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Kliniczna:",
                    "options": {
                        "Masowe, ponowne pobieranie krwi i wywiady od pacjentów (gigantyczne koszty i czas)": {"pat": +25, "avl": -10, "fin": -25, "comp": +10},
                        "Poleganie na wydrukach papierowych leżących na biurkach pielęgniarek": {"pat": -10, "avl": +5, "fin": +5, "comp": -10},
                    }
                },
                "Dir": {
                    "label": "Decyzja PR / Zarząd:",
                    "options": {
                        "Transparentne przyznanie się do ingerencji w dane, powiadomienie MZ i pacjentów": {"pat": +10, "avl": 0, "fin": -25, "comp": +30},
                        "Zatajenie manipulacji przed pacjentami, powołanie się na 'awarię techniczną'": {"pat": -10, "avl": 0, "fin": +10, "comp": -40},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Kret czy przejęte konto? (Środa, 10:00)",
            "desc": "Służby informują, że ataku dokonano z użyciem loginu ordynatora, który był ofiarą phishingu i nie miał włączonego uwierzytelniania dwuskładnikowego (MFA). Dziennikarze śledczy ujawniają sprawę.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Wymuszone, natychmiastowe wdrożenie MFA (kody SMS) dla wszystkich, mimo oporu personelu": {"pat": +10, "avl": -15, "fin": -10, "comp": +25},
                        "Tylko zresetowanie wszystkich haseł w szpitalu na 'silniejsze' (szybsze do wdrożenia)": {"pat": -15, "avl": +10, "fin": +5, "comp": -15},
                    }
                },
                "Med": {
                    "label": "Decyzja Lekarska:",
                    "options": {
                        "Wysłanie personelu na pilne szkolenie z cyber-higieny, kosztem opóźnień na izbie przyjęć": {"pat": +15, "avl": -10, "fin": -10, "comp": +15},
                        "Pozostawienie lekarzy przy pacjentach, przesłanie instrukcji bezpieczeństwa mailem": {"pat": -10, "avl": +15, "fin": +5, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Kadrowa:",
                    "options": {
                        "Ochrona zmanipulowanego ordynatora (był ofiarą), skupienie się na naprawie procesów": {"pat": 0, "avl": 0, "fin": 0, "comp": +15},
                        "Publiczne zwolnienie ordynatora dyscyplinarnie i zrzucenie na niego całej winy": {"pat": -5, "avl": 0, "fin": +10, "comp": -15},
                    }
                }
            }
        },
        4: {
            "title": "Runda 4: Rozliczenie z zaufania (Czwartek, 12:00)",
            "desc": "Kryzys opanowany, dane odtworzone. Szpital stoi jednak przed ogromnymi pozwami zbiorowymi od pacjentów, którym podano złe leki. MZ analizuje decyzje.",
            "questions": {
                "IT": {
                    "label": "Nowa Polityka IT:",
                    "options": {
                        "Wdrożenie systemu klasy DLP (Data Loss Prevention) i zaawansowanego monitorowania": {"pat": +15, "avl": +5, "fin": -25, "comp": +20},
                        "Brak zmian strukturalnych, uznanie incydentu za 'jednorazowy wypadek'": {"pat": -20, "avl": +10, "fin": +15, "comp": -30},
                    }
                },
                "Med": {
                    "label": "Relacje z Pacjentami:",
                    "options": {
                        "Uruchomienie darmowych badań kontrolnych dla pacjentów, których dane były zmanipulowane": {"pat": +25, "avl": -5, "fin": -30, "comp": +15},
                        "Oczekiwanie na indywidualne pozwy, brak proaktywnych działań rekompensacyjnych": {"pat": -10, "avl": +5, "fin": +10, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "Decyzja Strategiczna:",
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
            "desc": "Zewnętrzna chmura, do której szpital wysyła nocą zdjęcia TK do opisu, nagle przestaje odpowiadać. Równolegle, platforma do tele-monitorowania pacjentów kardiologicznych w domach zgłasza błąd API. Padli wasi główni dostawcy.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Natychmiastowe zerwanie tunelu VPN łączącego szpital z chmurą dostawcy (Air-Gap)": {"pat": 0, "avl": -20, "fin": -5, "comp": +15},
                        "Czekanie na odpowiedź supportu dostawcy. Utrzymywanie otwartych połączeń API": {"pat": -15, "avl": +5, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Wezwanie lokalnych radiologów na nadgodziny do szpitala, by opisywali zdjęcia na miejscu": {"pat": +20, "avl": +10, "fin": -25, "comp": +5},
                        "Wstrzymanie opisów planowych, diagnozowanie tylko przypadków 'na ratunek życia'": {"pat": -15, "avl": -10, "fin": +10, "comp": -5},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Aktywacja planu BCP: wdrożenie papierowych procedur dla pacjentów z telemonitoringu": {"pat": +15, "avl": 0, "fin": -10, "comp": +10},
                        "Brak aktywacji BCP, to 'tylko awaria po stronie dostawcy'": {"pat": -20, "avl": 0, "fin": +5, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "Runda 2: Zaraza po łączach (Środa, 22:00)",
            "desc": "Dostawca chmurowy komunikuje: padli ofiarą wirusa typu 'Worm', który replikuje się przez aktywne połączenia API. Wirus puka do waszych serwerów. Ponadto, wyciekły dane telemetryczne waszych pacjentów kardiologicznych.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Radykalne odcięcie całego szpitala od sieci Internet na 24h, aby skanować sieć wewnętrzną": {"pat": -10, "avl": -30, "fin": -15, "comp": +25},
                        "Pozostawienie szpitala w sieci, aktualizacja antywirusa i blokowanie tylko IP dostawcy": {"pat": -25, "avl": +15, "fin": 0, "comp": -20},
                    }
                },
                "Med": {
                    "label": "Decyzja Medyczna:",
                    "options": {
                        "Rozesłanie karetek i wezwanie najciężej chorych z telemonitoringu na oddział": {"pat": +30, "avl": 0, "fin": -30, "comp": +10},
                        "Wysłanie SMS-ów do pacjentów z prośbą o zgłoszenie się w razie złego samopoczucia": {"pat": -30, "avl": 0, "fin": +10, "comp": -15},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji (RODO):",
                    "options": {
                        "Zgłoszenie do UODO wycieku po stronie dostawcy, jako administrator danych": {"pat": +10, "avl": 0, "fin": -5, "comp": +30},
                        "Próba przerzucenia odpowiedzialności na dostawcę, brak zgłoszeń do UODO": {"pat": 0, "avl": 0, "fin": 0, "comp": -35},
                    }
                }
            }
        },
        3: {
            "title": "Runda 3: Odpowiedzialność (Czwartek, 08:00)",
            "desc": "Pacjenci są przerażeni wyciekiem danych. Media oskarżają szpital o 'oszczędzanie na bezpieczeństwie'. Szpital jest pozbawiony zdalnej radiologii, kolejki na SOR rosną.",
            "questions": {
                "IT": {
                    "label": "Decyzja IT:",
                    "options": {
                        "Wymuszenie na nowym dostawcy rygorystycznego audytu bezpieczeństwa przed umową": {"pat": +10, "avl": -10, "fin": -15, "comp": +25},
                        "Podpisanie umowy z najtańszym dostawcą bez audytów, aby szybko udrożnić opisy RTG": {"pat": -20, "avl": +25, "fin": +15, "comp": -30},
                    }
                },
                "Med": {
                    "label": "Decyzja Komunikacyjna:",
                    "options": {
                        "Osobiste telefony od lekarzy do zaniepokojonych pacjentów kardiologicznych": {"pat": +25, "avl": -5, "fin": -15, "comp": +15},
                        "Wydanie bezosobowego oświadczenia na stronie internetowej szpitala": {"pat": -15, "avl": 0, "fin": +5, "comp": -15},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Rozwiązanie umowy z winnym dostawcą i pozew sądowy o utracone korzyści": {"pat": +5, "avl": 0, "fin": +10, "comp": +15},
                        "Utrzymanie dostawcy, wynegocjowanie 'darmowego roku' w ramach rekompensaty": {"pat": -25, "avl": +10, "fin": +25, "comp": -25},
                    }
                }
            }
        },
        4: {
            "title": "Runda 4: Architektura Przyszłości (Piątek)",
            "desc": "Systemy powoli wracają. Ministerstwo Zdrowia domaga się raportu z zarządzania ryzykiem łańcucha dostaw. Zdarzenie uwidoczniło uzależnienie od jednej platformy.",
            "questions": {
                "IT": {
                    "label": "Nowa Architektura IT:",
                    "options": {
                        "Rozproszenie ryzyka: wdrożenie strategii Multi-Cloud z automatycznym zapasem": {"pat": +15, "avl": +20, "fin": -35, "comp": +20},
                        "Powrót do lokalnych serwerów (odrzucenie innowacji telemedycznych ze strachu)": {"pat": -10, "avl": -15, "fin": -10, "comp": -10},
                    }
                },
                "Med": {
                    "label": "Polityka Medyczna:",
                    "options": {
                        "Rygorystyczne, papierowe plany awaryjne dla każdej nowej technologii medycznej": {"pat": +20, "avl": 0, "fin": -10, "comp": +20},
                        "Poleganie całkowicie na technologii, redukcja klasycznego sprzętu diagnostycznego": {"pat": -25, "avl": +10, "fin": +20, "comp": -25},
                    }
                },
                "Dir": {
                    "label": "Decyzja Dyrekcji:",
                    "options": {
                        "Powołanie Działu Zarządzania Ryzykiem Stron Trzecich monitorującego vendorów": {"pat": +15, "avl": 0, "fin": -15, "comp": +25},
                        "Pozostawienie weryfikacji dostawców w rękach Działu Zakupów (skupionego na niskiej cenie)": {"pat": -20, "avl": 0, "fin": +15, "comp": -30},
                    }
                }
            }
        }
    }
}

# --- FUNKCJE POMOCNICZE ---
def calculate_score(team_name):
    # Punkty startowe
    pat, avl, fin, comp = 100, 100, 100, 100
    active_scenario_data = ALL_SCENARIOS[state["active_scenario"]]
    
    for r in range(1, state["round"] + 1):
        if r in state["teams"][team_name]["decisions"] and r in active_scenario_data:
            for role, choice in state["teams"][team_name]["decisions"][r].items():
                impact = active_scenario_data[r]["questions"][role]["options"][choice]
                pat += impact["pat"]
                avl += impact["avl"]
                fin += impact["fin"]
                comp += impact["comp"]
    return max(0, min(150, pat)), max(0, min(150, avl)), max(0, min(150, fin)), max(0, min(150, comp))

def render_progress_bar(label, value, is_critical=False):
    if is_critical:
        color = "green" if value > 80 else "orange" if value > 50 else "red"
    else:
        color = "green" if value > 70 else "orange" if value > 40 else "red"
        
    st.markdown(f"**{label}: {value}/150**")
    st.markdown(
        f"""<div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
        <div style="width: {min((value/150)*100, 100)}%; background-color: {color}; height: 24px; border-radius: 5px;"></div>
        </div>""", unsafe_allow_html=True
    )

# --- WIDOKI ---
def login_view():
    st.title("🏥 Cyberatak na Szpital - Symulacja (Wersja 5-wariantowa)")
    
    with st.expander("📱 Opcje dla Prowadzącego: Wyświetl kod QR"):
        game_url = st.text_input("Wklej tutaj link do aplikacji:")
        if game_url:
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={game_url}"
            st.image(qr_url, caption="Zeskanuj telefonem, aby dołączyć")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Wejście dla Zespołów")
        team_name = st.text_input("Podaj nazwę Szpitala:")
        if st.button("Dołącz do Sztabu"):
            if team_name:
                if team_name not in state["teams"]:
                    state["teams"][team_name] = {"decisions": {}, "ready": False}
                st.session_state["role"] = "team"
                st.session_state["team_name"] = team_name
                st.rerun()
            else:
                st.error("Wymagana nazwa szpitala!")
                
    with col2:
        st.subheader("Panel Koordynatora")
        admin_pass = st.text_input("Hasło (domyślnie: admin):", type="password")
        if st.button("Zaloguj jako Koordynator"):
            if admin_pass == "admin":
                st.session_state["role"] = "admin"
                st.rerun()
            else:
                st.error("Odmowa dostępu!")

def admin_view():
    st.title("👨‍⚕️ Panel Sterowania Symulacją")
    
    if state["round"] == 0:
        st.warning("Oczekuj na zalogowanie zespołów.")
        selected = st.selectbox("Wybierz scenariusz:", list(ALL_SCENARIOS.keys()), index=list(ALL_SCENARIOS.keys()).index(state["active_scenario"]))
        if selected != state["active_scenario"]:
            state["active_scenario"] = selected
            st.success(f"Zmieniono scenariusz na: {selected}")
    else:
        st.info(f"Trwa kryzys: **{state['active_scenario']}**")
    
    col1, col2 = st.columns(2)
    with col1:
        total_rounds = len(ALL_SCENARIOS[state["active_scenario"]])
        is_finished = state["round"] > total_rounds
        
        st.metric("Bieżąca Runda", state["round"] if not is_finished else "Raport Końcowy")
        
        if not is_finished:
            if st.button("Uruchom następną rundę ⏩", type="primary"):
                state["round"] += 1
                for t in state["teams"]: state["teams"][t]["ready"] = False
                st.rerun()
        else:
            if st.button("Zakończ dyżur i Resetuj 🔄"):
                state["round"] = 0
                state["teams"] = {}
                st.rerun()
                
    with col2:
        st.write("### Status Zespołów")
        if not state["teams"]:
            st.info("Brak podłączonych szpitali.")
        for t, data in state["teams"].items():
            status = "✅ Decyzje podjęte" if data["ready"] else "⏳ Narada sztabu..."
            st.write(f"- **{t}**: {status}")

    st.divider()
    st.write("### Tablica Monitorowania (KPI na żywo)")
    if state["teams"]:
        scores = []
        for t in state["teams"]:
            p, a, f, c = calculate_score(t)
            scores.append({"Placówka": t, "Zabezpieczenie Pacjentów": p, "Dostępność IT": a, "Finanse/PR": f, "Zgodność z Prawem": c})
        # Wersja bez .style.background_gradient zapobiega błędowi matplotlib w chmurze
        st.dataframe(pd.DataFrame(scores), use_container_width=True)

def team_view():
    team = st.session_state["team_name"]
    st.title(f"🚨 Sztab Kryzysowy: {team}")
    
    with st.sidebar:
        st.header("Stan Szpitala")
        p, a, f, c = calculate_score(team)
        render_progress_bar("❤️ Życie i Zdrowie Pacjentów", p, is_critical=True)
        render_progress_bar("🖥️ Dostępność Systemów", a)
        render_progress_bar("💰 Finanse i Wizerunek", f)
        render_progress_bar("⚖️ Compliance (MZ, RODO)", c)

    total_rounds = len(ALL_SCENARIOS[state["active_scenario"]])

    if state["round"] == 0:
        st.info("Trwa spokojny dyżur. Oczekujcie na start symulacji.")
        if st.button("Odśwież status"): st.rerun()
        
    elif 1 <= state["round"] <= total_rounds:
        r = state["round"]
        scenario = ALL_SCENARIOS[state["active_scenario"]][r]
        
        st.header(scenario["title"])
        st.error(f"**Raport z frontu:** {scenario['desc']}")
        
        if state["teams"][team]["ready"]:
            st.success("Procedury wdrożone. Czekajcie na rozwój wydarzeń (następna runda).")
            if st.button("Odśwież ekran"): st.rerun()
        else:
            st.write("---")
            st.write("### Wymagane pilne decyzje Sztabu:")
            
            with st.form(f"form_r{r}"):
                choices = {}
                for role, q_data in scenario["questions"].items():
                    st.subheader(q_data["label"])
                    choices[role] = st.radio(f"Wybór {role}", list(q_data["options"].keys()), label_visibility="collapsed")
                    st.write("")
                
                if st.form_submit_button("Wydaj Polecenia (Zatwierdź) 📝"):
                    if r not in state["teams"][team]["decisions"]:
                        state["teams"][team]["decisions"][r] = {}
                    state["teams"][team]["decisions"][r] = choices
                    state["teams"][team]["ready"] = True
                    st.rerun()

    elif state["round"] > total_rounds:
        st.header("🏁 Zakończenie Kryzysu - Raport Pokontrolny")
        p, a, f, c = calculate_score(team)
        
        st.subheader("Ocena placówki:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Bezpieczeństwo Pacjentów", p)
        col2.metric("Dostępność", a)
        col3.metric("Finanse/PR", f)
        col4.metric("Zgodność", c)
        
        st.write("---")
        if p < 50:
            st.error("Wyrok Prokuratora: **ZAGROŻENIE ŻYCIA PACJENTÓW.**")
        elif c < 50:
            st.error("Wyrok Regulatora: **KATASTROFA PRAWNA I KARY MILIONOWE.**")
        elif p >= 80 and c >= 80:
            st.success("Wyrok: **MISTRZOWSKIE ZARZĄDZANIE KRYZYSEM.**")
        else:
            st.info("Wyrok: **PRZETRWANIE Z GŁĘBOKIMI BLIZNAMI.** Szpital przetrwał, ale odbudowa reputacji potrwa lata.")

if "role" not in st.session_state:
    login_view()
elif st.session_state["role"] == "admin":
    admin_view()
elif st.session_state["role"] == "team":
    team_view()
