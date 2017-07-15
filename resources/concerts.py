# coding=utf-8
from datetime import datetime

CONCERTS = {
    'Cologne': {
        'area': 'Europe',
        'country': 'Germany',
        'venue': 'Lanxess Arena',
        'date': datetime(2017, 11, 8, 19, 0),
        'tickets': 'http://www.ticketmaster.de/artist/shakira-tickets/7142?cities=60108'
    },
    'Paris': {
        'area': 'Europe',
        'country': 'France',
        'venue': 'AccorHotels Arena',
        'date': datetime(2017, 11, 10, 19, 0),
        'tickets': 'https://www.ticketmaster.fr/fr/manifestation/shakira-billet/idmanif/405762'
    },
    'Luxembourg': {
        'area': 'Europe',
        'country': 'Luxembourg',
        'venue': 'Rockhal',
        'date': datetime(2017, 11, 11, 19, 0),
        'tickets': 'https://www.etix.com/ticket/p/3584865/shakira-el-dorado-world-tour-eschalzette-rockhal-luxembourg'
    },
    'Antwerp': {
        'area': 'Europe',
        'country': 'Belgium',
        'venue': 'Sportpaleis',
        'date': datetime(2017, 11, 12, 19, 0),
        'tickets': 'https://www.teleticketservice.com/en/tickets/2017-2018/shakira-the-el-dorado-tour'
    },
    'Amsterdam': {
        'area': 'Europe',
        'country': 'Netherlands',
        'venue': 'Ziggo Dome',
        'date': datetime(2017, 11, 14, 19, 0),
        'tickets': 'http://www.ticketmaster.nl/event/shakira-el-dorado-world-tour-tickets/190881'
    },
    'Montpellier': {
        'area': 'Europe',
        'country': 'France',
        'venue': 'Park & Suites Arena',
        'date': datetime(2017, 11, 16, 19, 0),
        'tickets': 'https://www.ticketmaster.fr/fr/manifestation/shakira-billet/idmanif/406502'
    },
    'Bilbao': {
        'area': 'Europe',
        'country': 'Spain',
        'venue': 'BEC',
        'date': datetime(2017, 11, 17, 19, 0),
        'tickets': 'https://www.livenation.es/artist/shakira-tickets'
    },
    'Madrid': {
        'area': 'Europe',
        'country': 'Spain',
        'venue': 'WiZink Centre',
        'date': datetime(2017, 11, 19, 19, 0),
        'tickets': 'https://www.livenation.es/show/996061/shakira-el-dorado-world-tour/madrid/2017-11-19'
    },
    'Lisbon': {
        'area': 'Europe',
        'country': 'Portugal',
        'venue': 'MEO Arena',
        'date': datetime(2017, 11, 22, 19, 0),
        'tickets': 'http://www.blueticket.pt/Event/3150'
    },
    'A Coruna': {
        'area': 'Europe',
        'country': 'Spain',
        'venue': 'Coliseum',
        'date': datetime(2017, 11, 23, 19, 0),
        'tickets': 'https://www.livenation.es/show/996071/shakira-el-dorado-world-tour/a%20coru%C3%B1a/2017-11-23'
    },
    'Barcelona': {
        'area': 'Europe',
        'country': 'Spain',
        'venue': 'Palau San Jordi',
        'date': datetime(2017, 11, 25, 19, 0),
        'tickets': 'https://www.livenation.es/show/996064/shakira-el-dorado-world-tour/barcelona/2017-11-25'
    },
    'Lyon': {
        'area': 'Europe',
        'country': 'France',
        'venue': 'Halle Tony Garnier',
        'date': datetime(2017, 11, 28, 19, 0),
        'tickets': 'https://www.ticketmaster.fr/fr/manifestation/shakira-billet/idmanif/406508/idtier/4827637'
    },
    'Munich': {
        'area': 'Europe',
        'country': 'Germany',
        'venue': 'Olympiahalle',
        'date': datetime(2017, 11, 30, 19, 0),
        'tickets': 'http://www.ticketmaster.de/artist/shakira-tickets/7142?cities=60135'
    },
    'Zurich': {
        'area': 'Europe',
        'country': 'Switzerland',
        'venue': 'Hallenstadion',
        'date': datetime(2017, 12, 1, 19, 0),
        'tickets': 'http://www.ticketcorner.ch/tickets.html?fun=evdetail&affiliate=BIT&doc=evdetailb&key=1939371%249783886'
    },
    'Milan': {
        'area': 'Europe',
        'country': 'Italy',
        'venue': 'Medionlanum Forum',
        'date': datetime(2017, 12, 3, 19, 0),
        'tickets': 'http://www.ticketone.it/shakira-biglietti.html?affiliate=ITT&doc=artistPages/tickets&fun=artist&action=tickets&kuid=462895'
    },
    'Orlando': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Amway Center',
        'date': datetime(2018, 1, 9, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-orlando-florida-01-09-2018/event/220052CF9A107C84'
    },
    'Sunrise': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'BB&T',
        'date': datetime(2018, 1, 11, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-sunrise-florida-01-11-2018/event/0D0052CE89FE7F36'
    },
    'Miami': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'American Airlines Arena',
        'date': datetime(2018, 1, 12, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-miami-florida-01-12-2018/event/0D0052D0726473FF'
    },
    'Washington DC': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Verizon Centre',
        'date': datetime(2018, 1, 16, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-washington-district-of-columbia-01-16-2018'
    },
    'New York': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Madison Square Garden',
        'date': datetime(2018, 1, 17, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-new-york-new-york-01-17-2018/event/3B0052D0DB4423FA'
    },
    'Montreal': {
        'area': 'North America',
        'country': 'Canada',
        'venue': 'Bell Centre',
        'date': datetime(2018, 1, 19, 19, 0),
        'tickets': 'http://www.evenko.ca/en/events/12813/shakira/bell-centre/01-19-2018'
    },
    'Toronto': {
        'area': 'North America',
        'country': 'Canada',
        'venue': 'Air Canada Centre',
        'date': datetime(2018, 1, 20, 19, 0),
        'tickets': 'https://www.ticketmaster.ca/shakira-el-dorado-world-tour-toronto-ontario-01-20-2018/event/100052D6AED82EEC'
    },
    'Detroit': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Little Ceasars',
        'date': datetime(2018, 1, 22, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-detroit-michigan-01-22-2018/event/080052D69C23292E'
    },
    'Chicago': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'United Center',
        'date': datetime(2018, 1, 23, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-chicago-illinois-01-23-2018/event/040052B9CBAA229C'
    },
    'Houston': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Toyota Center',
        'date': datetime(2018, 1, 26, 19, 0),
        'tickets': 'http://www.houstontoyotacenter.com/events/detail/shakira'
    },
    'Dallas': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'American Airlines Center',
        'date': datetime(2018, 1, 28, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-dallas-texas-01-28-2018/event/0C0052CFE98C44D7'
    },
    'San Antonio': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'AT&T Center',
        'date': datetime(2018, 1, 29, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-san-antonio-texas-01-29-2018/event/3A0052D7AC2538F1'
    },
    'Los Angeles': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'The Forum',
        'date': datetime(2018, 2, 1, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-inglewood-california-02-01-2018/event/090052D412363FF5'
    },
    'Phoenix': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Talking Stick Resort Arena',
        'date': datetime(2018, 2, 3, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-phoenix-arizona-02-03-2018/event/190052CEA5C31E81'
    },
    'Anaheim': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Honda Center',
        'date': datetime(2018, 2, 6, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-anaheim-california-02-06-2018/event/090052D0C4B265C8'
    },
    'San Jose': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'SAP Center',
        'date': datetime(2018, 2, 7, 19, 0),
        'tickets': 'https://www1.ticketmaster.com/shakira-el-dorado-world-tour-san-jose-california-02-07-2018/event/1C0052D0CB3E8ED1'
    },
    'San Diego': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'Valley View Casino Center',
        'date': datetime(2018, 2, 9, 19, 0),
        'tickets': 'https://www.axs.com/events/338294/shakira-tickets'
    },
    'Las Vegas': {
        'area': 'North America',
        'country': 'United States',
        'venue': 'MGM Grand',
        'date': datetime(2018, 2, 10, 19, 0),
        'tickets': 'https://www.axs.com/events/338054/shakira-tickets?skin=grandgarden'
    }
}
