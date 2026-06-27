"""
LexGuard AI — Database Seeder
Run: python database/seed.py
Seeds LegalCases and Lawyers tables with sample Indian law data.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app
from app import db
from app.models.legal_case import LegalCase
from app.models.lawyer import Lawyer


SAMPLE_CASES = [
    {
        "title": "Maneka Gandhi v. Union of India (1978)",
        "act_name": "Constitution of India",
        "section": "Article 21",
        "year": 1978,
        "court": "Supreme Court of India",
        "summary": "Landmark case expanding Article 21 right to life and personal liberty. Held that the procedure for depriving a person of personal liberty must be fair, just and reasonable.",
        "judgement_text": "The word 'law' in Article 21 must be just, fair, and reasonable law. Maneka Gandhi's passport confiscation violated fundamental rights.",
        "keywords": "right to life personal liberty passport fundamental rights article 21 due process",
    },
    {
        "title": "Vishakha v. State of Rajasthan (1997)",
        "act_name": "Constitution of India / POSH",
        "section": "Articles 14, 19, 21",
        "year": 1997,
        "court": "Supreme Court of India",
        "summary": "Landmark judgment that laid down Vishakha Guidelines for prevention of sexual harassment at the workplace. Led to enactment of POSH Act 2013.",
        "judgement_text": "Sexual harassment at workplace violates fundamental rights. Employers must constitute committees to address complaints of sexual harassment.",
        "keywords": "sexual harassment workplace guidelines vishakha posh act women rights employer",
    },
    {
        "title": "K.S. Puttaswamy v. Union of India (2017)",
        "act_name": "Constitution of India",
        "section": "Article 21",
        "year": 2017,
        "court": "Supreme Court of India",
        "summary": "Nine-judge bench unanimously held that the right to privacy is a fundamental right protected under Article 21 of the Constitution. Challenged Aadhaar biometric data collection.",
        "judgement_text": "Privacy is a fundamental right intrinsic to human dignity and liberty. Informational privacy, decisional autonomy, and bodily integrity are all protected.",
        "keywords": "right to privacy fundamental right aadhaar data protection article 21 information",
    },
    {
        "title": "Shayara Bano v. Union of India (2017)",
        "act_name": "Muslim Personal Law",
        "section": "Triple Talaq",
        "year": 2017,
        "court": "Supreme Court of India",
        "summary": "Supreme Court declared instant Triple Talaq (talaq-e-biddat) unconstitutional as it violates Articles 14 and 21 of the Constitution, being manifestly arbitrary.",
        "judgement_text": "The practice of triple talaq is manifestly arbitrary and unconstitutional. A man cannot divorce his wife by uttering talaq thrice in one sitting.",
        "keywords": "triple talaq muslim personal law divorce women rights unconstitutional article 14",
    },
    {
        "title": "Arnesh Kumar v. State of Bihar (2014)",
        "act_name": "IPC 498A CrPC 41",
        "section": "IPC 498A",
        "year": 2014,
        "court": "Supreme Court of India",
        "summary": "Directed that police cannot automatically arrest under IPC Section 498A (matrimonial cruelty). Police must apply their mind before arrest. Magistrates must record reasons before remanding accused.",
        "judgement_text": "Arrest brings humiliation, curtails freedom, casts scars forever. Police should not arrest routinely under 498A. Checklist must be followed before arrest.",
        "keywords": "arrest ipc 498a matrimonial cruelty domestic violence police powers section 41 crpc",
    },
    {
        "title": "Olga Tellis v. Bombay Municipal Corporation (1985)",
        "act_name": "Constitution of India",
        "section": "Article 21",
        "year": 1985,
        "court": "Supreme Court of India",
        "summary": "Held that the right to livelihood is part of the right to life under Article 21. The eviction of pavement dwellers without alternative accommodation was held unconstitutional.",
        "judgement_text": "The right to life includes the right to livelihood. No person can be deprived of livelihood without legal process. Pavement dwellers cannot be evicted without rehabilitation.",
        "keywords": "right to livelihood homeless eviction pavement article 21 shelter fundamental rights",
    },
    {
        "title": "Ratio Decidendi in State of Maharashtra v. M.H. George (1965)",
        "act_name": "Foreign Exchange Regulation Act",
        "section": "FERA",
        "year": 1965,
        "court": "Supreme Court of India",
        "summary": "Case involving financial violations and smuggling of gold. Established principles of mens rea (criminal intent) in statutory offences under the Foreign Exchange Act.",
        "judgement_text": "Mens rea is generally presumed unless excluded expressly or by necessary implication. Economic offences may have strict liability under specific statutes.",
        "keywords": "mens rea criminal intent forex gold smuggling statutory offence strict liability financial crime",
    },
    {
        "title": "State of West Bengal v. Anwar Ali Sarkar (1952)",
        "act_name": "Constitution of India",
        "section": "Article 14",
        "year": 1952,
        "court": "Supreme Court of India",
        "summary": "Landmark case on Article 14 right to equality. Struck down the West Bengal Special Courts Act as it allowed arbitrary classification of cases without reasonable nexus.",
        "judgement_text": "Article 14 strikes at arbitrariness. Classification must be based on intelligible differentia having a reasonable nexus to the object sought to be achieved.",
        "keywords": "equality article 14 reasonable classification arbitrary law discrimination special courts",
    },
    {
        "title": "Nandini Satpathy v. P.L. Dani (1978)",
        "act_name": "CrPC / Constitutional Law",
        "section": "Article 20(3)",
        "year": 1978,
        "court": "Supreme Court of India",
        "summary": "Expanded the right against self-incrimination. Held that an accused cannot be compelled to answer questions that might incriminate them, even during investigation.",
        "judgement_text": "The right against self-incrimination extends to pre-trial and investigation stages. A person cannot be compelled to be a witness against himself under Article 20(3).",
        "keywords": "self incrimination article 20 right to silence accused investigation police questioning fundamental right",
    },
    {
        "title": "Hussainara Khatoon v. State of Bihar (1979)",
        "act_name": "CrPC / Constitutional Law",
        "section": "Article 21",
        "year": 1979,
        "court": "Supreme Court of India",
        "summary": "PIL case that exposed thousands of undertrial prisoners languishing in Bihar jails for years without trial. Established right to speedy trial as fundamental right.",
        "judgement_text": "Right to speedy trial is implicit in Article 21. Undertrial prisoners cannot be kept in custody for periods exceeding maximum sentence for the alleged offence.",
        "keywords": "speedy trial undertrial prisoners bail right to life article 21 prison judicial delay",
    },
    {
        "title": "MC Mehta v. Union of India (1987)",
        "act_name": "Environmental Law",
        "section": "Article 21 / Absolute Liability",
        "year": 1987,
        "court": "Supreme Court of India",
        "summary": "Introduced the doctrine of Absolute Liability — enterprises engaged in inherently dangerous activities are absolutely liable for harm regardless of negligence or care.",
        "judgement_text": "Where an enterprise is engaged in a hazardous activity and harm results, the enterprise is absolutely liable. There are no exceptions to this rule unlike strict liability.",
        "keywords": "absolute liability environmental pollution hazardous industry oleum gas leak compensation tort",
    },
    {
        "title": "S.R. Bommai v. Union of India (1994)",
        "act_name": "Constitution of India",
        "section": "Article 356",
        "year": 1994,
        "court": "Supreme Court of India",
        "summary": "Significantly curtailed the power of the Centre to dismiss State governments under Article 356 (President's Rule). Held that the floor test must precede dismissal.",
        "judgement_text": "Article 356 is not a political weapon. President's Rule must be based on objective material. Floor test is the democratic way to test majority. Courts can review the proclamation.",
        "keywords": "presidents rule article 356 state government dismissal floor test federalism constitutional law",
    },
    {
        "title": "Indra Sawhney v. Union of India (1992)",
        "act_name": "Constitution of India",
        "section": "Article 16 OBC Reservations",
        "year": 1992,
        "court": "Supreme Court of India",
        "summary": "Nine-judge bench upheld 27% OBC reservation (Mandal Commission report) but imposed 50% ceiling on reservations and excluded the 'creamy layer' from OBC benefits.",
        "judgement_text": "50% ceiling on reservations is inviolable. Creamy layer must be excluded from OBC reservations. Reservation in promotions is not permissible under the original Constitution.",
        "keywords": "obc reservation mandal commission article 16 creamy layer 50 percent ceiling equality backward class",
    },
    {
        "title": "Shreya Singhal v. Union of India (2015)",
        "act_name": "IT Act 2000",
        "section": "Section 66A",
        "year": 2015,
        "court": "Supreme Court of India",
        "summary": "Struck down Section 66A of the IT Act which criminalized sending offensive messages online. Held it to be unconstitutionally vague and violative of free speech under Article 19.",
        "judgement_text": "Section 66A is struck down in its entirety as unconstitutional. Terms like offensive, menacing, annoying are vague and have a chilling effect on free speech.",
        "keywords": "section 66a internet freedom free speech it act offensive message online censorship article 19",
    },
    {
        "title": "Joseph Shine v. Union of India (2018)",
        "act_name": "IPC",
        "section": "Section 497",
        "year": 2018,
        "court": "Supreme Court of India",
        "summary": "Unanimously struck down Section 497 IPC (Adultery) as unconstitutional. Held that a woman's sexuality cannot be controlled by her husband and the law was based on gender stereotypes.",
        "judgement_text": "Section 497 is unconstitutional as it treats women as property of their husbands, violating Articles 14, 15, and 21. Adultery may be a ground for divorce but not a crime.",
        "keywords": "adultery section 497 ipc unconstitutional gender equality women rights marriage sexuality article 14 15 21",
    },
]

SAMPLE_LAWYERS = [
    {
        "name": "Adv. Priya Nair",
        "specialization": "Criminal Law",
        "location": "Chennai",
        "contact": "+91-98401-12345",
        "email": "priya.nair@lexguard.example",
        "rating": 4.8,
        "experience_years": 12,
        "bio": "Senior criminal lawyer with 12+ years experience in Madras High Court. Specializes in bail applications, criminal trials, and POCSO cases.",
        "avatar_initials": "PN",
    },
    {
        "name": "Adv. Rajesh Kumar Singh",
        "specialization": "Property Law",
        "location": "Delhi",
        "contact": "+91-98110-56789",
        "email": "rajesh.singh@lexguard.example",
        "rating": 4.6,
        "experience_years": 18,
        "bio": "Expert in property registration, title disputes, RERA matters, and real estate litigation in Delhi courts.",
        "avatar_initials": "RK",
    },
    {
        "name": "Adv. Meena Krishnamurthy",
        "specialization": "Family Law",
        "location": "Bengaluru",
        "contact": "+91-80-23456789",
        "email": "meena.k@lexguard.example",
        "rating": 4.9,
        "experience_years": 15,
        "bio": "Compassionate family lawyer handling divorce, custody, domestic violence, and matrimonial property disputes in Karnataka courts.",
        "avatar_initials": "MK",
    },
    {
        "name": "Adv. Faisal Ahmed",
        "specialization": "Cyber Law",
        "location": "Hyderabad",
        "contact": "+91-40-98765432",
        "email": "faisal.ahmed@lexguard.example",
        "rating": 4.7,
        "experience_years": 9,
        "bio": "Tech-savvy cyber lawyer handling online fraud, hacking cases, IT Act violations, and digital privacy matters.",
        "avatar_initials": "FA",
    },
    {
        "name": "Adv. Sunita Sharma",
        "specialization": "Labor & Employment Law",
        "location": "Mumbai",
        "contact": "+91-22-12345678",
        "email": "sunita.sharma@lexguard.example",
        "rating": 4.5,
        "experience_years": 20,
        "bio": "Experienced labor attorney handling wrongful termination, industrial disputes, ESIC/EPF matters, and workplace harassment cases in Bombay High Court.",
        "avatar_initials": "SS",
    },
    {
        "name": "Adv. Anand Patel",
        "specialization": "Corporate & Contract Law",
        "location": "Ahmedabad",
        "contact": "+91-79-87654321",
        "email": "anand.patel@lexguard.example",
        "rating": 4.4,
        "experience_years": 14,
        "bio": "Corporate lawyer specializing in company registration, contracts, M&A, IPO compliance, and investor agreements.",
        "avatar_initials": "AP",
    },
    {
        "name": "Adv. Lakshmi Rajan",
        "specialization": "Consumer Law",
        "location": "Chennai",
        "contact": "+91-44-65432109",
        "email": "lakshmi.rajan@lexguard.example",
        "rating": 4.6,
        "experience_years": 11,
        "bio": "Fights for consumer rights in District Consumer Forums and NCDRC. Handles e-commerce fraud, product liability, and service deficiency cases.",
        "avatar_initials": "LR",
    },
    {
        "name": "Adv. Mohammed Irfan",
        "specialization": "Criminal Law",
        "location": "Kolkata",
        "contact": "+91-33-76543210",
        "email": "irfan.kolkata@lexguard.example",
        "rating": 4.3,
        "experience_years": 8,
        "bio": "Criminal defense lawyer in Calcutta High Court. Handles NDPS cases, cheating, forgery, and bail matters.",
        "avatar_initials": "MI",
    },
    {
        "name": "Adv. Deepa Venkataraman",
        "specialization": "Intellectual Property",
        "location": "Bengaluru",
        "contact": "+91-80-34567890",
        "email": "deepa.ip@lexguard.example",
        "rating": 4.8,
        "experience_years": 13,
        "bio": "Specializes in patent filing, trademark registration, copyright disputes, and IP litigation in Indian courts and the IP Office.",
        "avatar_initials": "DV",
    },
    {
        "name": "Adv. Sanjay Mishra",
        "specialization": "Tax Law",
        "location": "Delhi",
        "contact": "+91-11-23456780",
        "email": "sanjay.taxlaw@lexguard.example",
        "rating": 4.5,
        "experience_years": 22,
        "bio": "Tax attorney and chartered accountant handling income tax appeals, GST disputes, customs cases, and ITAT litigation.",
        "avatar_initials": "SM",
    },
]


def seed():
    with app.app_context():
        db.create_all()

        # Seed LegalCases
        if LegalCase.query.count() == 0:
            print("🌱 Seeding legal cases...")
            for case_data in SAMPLE_CASES:
                case = LegalCase(**case_data)
                db.session.add(case)
            db.session.commit()
            print(f"✅ {len(SAMPLE_CASES)} legal cases seeded.")
        else:
            print("ℹ️  Legal cases already exist, skipping.")

        # Seed Lawyers
        if Lawyer.query.count() == 0:
            print("🌱 Seeding lawyers...")
            for lawyer_data in SAMPLE_LAWYERS:
                lawyer = Lawyer(**lawyer_data)
                db.session.add(lawyer)
            db.session.commit()
            print(f"✅ {len(SAMPLE_LAWYERS)} lawyers seeded.")
        else:
            print("ℹ️  Lawyers already exist, skipping.")

        print("🎉 Database seeding complete!")


if __name__ == "__main__":
    seed()
