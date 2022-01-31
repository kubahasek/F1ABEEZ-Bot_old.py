import os
from dotenv import load_dotenv

load_dotenv()

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabaseURL = os.environ.get("incidentDatabaseURL")
profileDatabaseURL = os.environ.get("profileDatabaseURL")
incidentDatabaseId = os.environ.get("incidentDatabaseId")
appealsDatabaseURL = os.environ.get("appealsDatabaseURL")
appealsDatabaseId = os.environ.get("appealsDatabaseId")
mongoDBConnSTR = os.environ.get("mongoDBConnSTR")
figmaToken = os.environ.get("figma_token")
    
color = 16236412
banChannel = 853679513406013460
warningChannel = 909158996592713758
welcomeChannel = 838841316519313408
stewardsAnnoucementChannel = 864564506368933888
generalAnnoucementChannel = 774696889424805891
socialMediaAnnouncementChannel = 834548053704572948
incidentReportChannel = 871334405359144970
appealReportChannel = 871334445716766800
suggestionSubmitChannel = 877977932914651176
incidentLogChannel = 861939856481189908
suggestionLogChannel = 919200817075073055
leavingChannel = 774605933661257729

tier1Role = 795227294766727169
reserveTier1Role = 893654550962139176
tier2Role = 795227317684928546
reserveTier2Role = 893654646462218240
tier3Role = 813703851349245965
reserveTier3Role = 893654551704526859
tierMRole = 840694396990521364
reserveTierMRole = 893654640321789983
nationsLeagueRole = 893765015776161854
academyRole = 774740889557270539