from connector.telegram_connector import send_message_tele,send_file_tele
from analysis.bot import *
from connector.api_connector import get_token,get_list_stock,get_asset
import json
from common.helper import read_config
from collections import defaultdict 
from datetime import datetime
from connector.io import write_to_csv
NUMBER_THREAD = 8
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


# pool = Pool()
import platform
import time
os_name = platform.system()

def beautify_list_rated_symbol(list_rated_symbol):
    result = ""
    count = 0 
    for rating, symbols in list_rated_symbol.items():
        count += len(symbols)
        result += f"Hang ngon {rating}* (size: {len(symbols)}):\n"
        for symbol in symbols:
            result += f"{symbol}\n"
        result += "\n"  # Add an empty line after each rating
    result = f"Tong so luong ma ({count}) \n {result}"
    return result

def beauty_print(data, account = "Tai khoan Minh dang cam : "):
    result = account +"\n"
    for key, value in data.items():
        if key in ('Cash', 'Margin'):
            result += f"{key}: {value:.2%}\n"
        else:
            result += f"{key}: {value['proportion']:.2%}. Biến động tính đến hiện tại : {(value['current_value'] - value['cost_value'])/value['cost_value']:.2%} \n"
    return result
def check_buy_bot(beautify_list_rated_symbol,list_symbol_string):
    # list_symbol_string = 'CTR,TNG,NTL,NLG,VHM,PNJ,VHC,DIG,DPR, IDC, SZC,KBC, HCM'
    list_symbol = list_symbol_string.split(',')
    list_symbol_pass = []
    for symbol in list_symbol:
        try:
            symbol = symbol.strip()
            week_criteria = check_week(symbol)
            if week_criteria:
                list_symbol_pass.append(symbol)
        except:
            pass

    list_symbol_pass_volume =[]
    for symbol in list_symbol_pass:
        try:
            volume_ok_and_can_buy = check_volume_day_and_can_buy(symbol)
            if volume_ok_and_can_buy:
                list_symbol_pass_volume.append(symbol)
        except:
            pass
    list_symbol_has_money = []
    for symbol in list_symbol_pass_volume:
        try:
            money_flow = check_money_flow(symbol)
            if len(money_flow) >=10:
                list_symbol_has_money.append(symbol)
        except:
            pass
    list_symbol_strong = []
    list_symbol_trading = []
    for symbol in list_symbol_has_money:
        try:
            is_strong = check_strong_stock(symbol)
            if is_strong :
                list_symbol_strong.append(symbol)
            elif trading_symbol(symbol) or check_poc(symbol):
                list_symbol_trading.append(symbol)
        except:
            pass
    list_rated_symbol = defaultdict(list) 
    for symbol in list_symbol_strong:
        try:
            rating = squeez_on(symbol)
            list_rated_symbol[rating].append(symbol)
        except:
            pass
    write_to_csv(list_rated_symbol[9])
    send_file_tele('result.csv')
    # print(datetime.now().date(),list_rated_symbol[0])
    send_message_tele(beautify_list_rated_symbol(list_rated_symbol))
    send_message_tele("Lieu an nhieu (Co the quan sat bat day) \n" + '\n'.join(list_symbol_trading))

def check_account(beauty_print):
    config = read_config('./configurations.ini')
    hold_list_bot = []
    user_bot = config['tcbs-bot']['USER']
    password_bot= config['tcbs-bot']['PASS']
    url_bot= config['tcbs-bot']['URL']

    payload_bot = json.dumps({
        "username": user_bot,
        "password": password_bot
    })
    token_bot = get_token(payload_bot)
    print(token_bot)
    data_bot = get_asset(token_bot)
    send_message_tele(beauty_print(data_bot, "Tai khoan BOT dang cam : "))
    list_stock_bot = get_list_stock(token_bot,url_bot)
    # list_stock = {'stock':[{'symbol' : 'IDC'},{'symbol' : 'VCG'},{'symbol' : 'VGC'},{'symbol' : 'PVD'},{'symbol' : 'DCM'}]}

    for symbol in list_stock_bot['stock']:
        hold_list_bot.append(symbol['symbol'])
    list_symbol_sell_bot = []
    for symbol in hold_list_bot:
        symbol = symbol.strip()
        check_sell_result = check_sell(symbol)
        if check_sell_result:
            list_symbol_sell_bot.append(symbol)
    print(get_asset(token_bot))

    # print(list_stock)
    send_message_tele(f'\n Danh sach khuyen nghi ban ({len(list_symbol_sell_bot)}): \n' + '\n'.join(list_symbol_sell_bot))
    send_message_tele("-----------------------------------------------------------")

    send_message_tele("------------------------------------------------------------")
    config = read_config('./configurations.ini')
    hold_list = []
    user = config['tcbs']['USER']
    password= config['tcbs']['PASS']
    url= config['tcbs']['URL']

    payload = json.dumps({
        "username": user,
        "password": password
    })
    token = get_token(payload)
    print(token)
    list_stock = get_list_stock(token,url)
    # list_stock = {'stock':[{'symbol' : 'IDC'},{'symbol' : 'VCG'},{'symbol' : 'VGC'},{'symbol' : 'PVD'},{'symbol' : 'DCM'}]}
    data = get_asset(token)
    send_message_tele(beauty_print(data))
    for symbol in list_stock['stock']:
        hold_list.append(symbol['symbol'])
    list_symbol_sell = []
    for symbol in hold_list:
        symbol = symbol.strip()
        check_sell_result = check_sell(symbol)
        if check_sell_result:
            list_symbol_sell.append(symbol)

    print(list_stock)
    send_message_tele(f'\n Danh sach khuyen nghi ban ({len(list_symbol_sell)}): \n' + '\n'.join(list_symbol_sell))
    send_message_tele("------------------------------------------------------------")


import sys
if __name__ == '__main__':
    list_symbol_string = "BAF,AAV,ABT,ACM,ADC,AGC,ALT,AMC,AME,AMV,API,APP,APS,ARM,ART,ASG,ATS,AVS,BAB,BAX,BBC,BBS,BCC,BCF,BDB,BED,BII,BKC,BLF,BNA,BPC,BSC,BSI,BST,BTS,BTW,BVS,BXH,C69,C92,CAG,CAN,CAP,CAV,CDN,CEO,CET,CIA,CIC,CJC,CKV,CLH,CLM,CMC,CMS,CPC,CSC,CTB,CTC,CTM,CTP,CTT,CTV,CTX,CVN,CX8,D11,DAD,DAE,DC2,DDG,DGL,DHI,DHL,DHP,DHT,DIH,DL1,DNC,DNM,DNP,DP3,DPC,DS3,DST,DTD,DTK,DVG,DXP,DXS,DZM,E1SSHN30,EBA,EBS,ECI,EID,EVS,FDT,FID,FTV,GBS,GDW,GFC,GHA,GIC,GKM,GLT,GMA,GMX,HAD,HAP,HAT,HBB,HBE,HBS,HCC,HCT,HDA,HEV,HGM,HHC,HHG,HHL,HJS,HKT,HLC,HLD,HMH,HNM,HOM,HPC,HPM,HPR,HPS,HSC,HST,HTB,HTC,HTP,HUT,HVT,ICG,IDC,IDJ,IDV,INC,INN,ITQ,IVS,KBT,KDM,KHG,KHS,KKC,KLF,KLS,KMF,KMT,KSD,KSQ,KST,KTS,KTT,KVC,L14,L18,L35,L40,L43,L61,L62,LAF,LAS,LBE,LCD,LCS,LDP,LHC,LIG,LM7,LUT,MAC,MAS,MAX,MBG,MBS,MCC,MCF,MCL,MCO,MDC,MED,MEL,MHL,MIH,MIM,MKV,MNC,MSC,MST,MVB,NAG,NAP,NBC,NBP,NBW,NDN,NDX,NET,NFC,NHC,NIS,NLC,NRC,NSC,NSH,NSN,NST,NTH,NTP,NVB,NVC,OCH,ONE,PAN,PBP,PCE,PCG,PCT,PDB,PDC,PEN,PGN,PGS,PGT,PHN,PHP,PIA,PIC,PJC,PLC,PMB,PMC,PMP,PMS,POT,PPE,PPP,PPS,PPY,PRC,PRE,PSC,PSD,PSE,PSI,PSW,PTD,PTI,PTS,PV2,PVB,PVC,PVG,PVI,PVL,PVS,QBS,QHD,QST,QTC,RCL,RHC,S55,S64,S91,S99,SAF,SCI,SD2,SD4,SD5,SD6,SD9,SDA,SDC,SDG,SDN,SDS,SDT,SDU,SEB,SED,SEL,SFN,SGC,SGD,SGH,SHB,SHE,SHN,SHS,SHT,SIC,SJ1,SJE,SKS,SLS,SME,SMN,SMT,SNG,SPI,SRA,SSC,SSM,SSS,STC,STP,SVN,SVS,SZB,TA9,TAR,TAS,TBX,TC6,TDN,TDT,TET,TFC,THB,THD,THI,THS,THT,THV,TIG,TJC,TKC,TKU,TLC,TMB,TMC,TMX,TNG,TPH,TPP,TSB,TSM,TST,TTC,TTH,TTL,TTT,TTZ,TV3,TV4,TVB,TVC,TVD,TXM,UNI,V12,V21,VAT,VBC,VC1,VC2,VC3,VC6,VC7,VC9,VCC,VCH,VCM,VCS,VCV,VDL,VE1,VE2,VE3,VE4,VE8,VFG,VGP,VGS,VHE,VHL,VIE,VIF,VIG,VIT,VKC,VLA,VMC,VMS,VNC,VND,VNF,VNR,VNT,VSA,VSM,VTC,VTH,VTJ,VTL,VTV,VXB,WCS,WSS,X20,YSC,AAA,AAM,AAT,ABS,ACB,ACC,ACL,ADG,ADS,AGD,AGG,AGM,AGR,AHP,ALP,AMD,ANC11601,ANV,APC,APG,APH,ASIAGF,ASM,ASP,AST,BAS,BCE,BCG,BCI,BCM,BFC,BGM,BHN,BHS,BIC,BID,BKG,BMC,BMI,BMP,BRC,BTP,BTT,BVH,BWE,C32,C47,CCI,CCL,CDC,CEE,CFPT2016,CFPT2101,CHP,CHPG2020,CHPG2101,CHPG2102,CHPG2103,CHPG2104,CHPG2105,CHPG2106,CHPG2107,CHPG2108,CIG,CII,CII11709,CII41401,CKDH2002,CKDH2101,CKDH2102,CKG,CLC,CLL,CLP,CLW,CMBB2010,CMBB2101,CMG,CMSN2101,CMSN2102,CMSN2103,CMV,CMWG2013,CMWG2016,CMWG2101,CMWG2102,CMWG2103,CMWG2104,CMWG2105,CMX,CNG,CNVL2003,CNVL2101,CNVL2102,COM,CPDR2101,CPDR2102,CPNJ2101,CPNJ2102,CPNJ2103,CRC,CRE,CREE2101,CSBT2101,CSG,CSM,CSTB2007,CSTB2010,CSTB2014,CSTB2101,CSTB2102,CSTB2103,CSTB2104,CSV,CTCB2012,CTCB2101,CTCB2102,CTCB2103,CTCB2104,CTCH2003,CTCH2102,CTCH2103,CTD,CTF,CTG,CTI,CTS,CVHM2008,CVHM2101,CVHM2102,CVHM2103,CVHM2104,CVHM2105,CVHM2106,CVIC2005,CVIC2101,CVIC2102,CVIC2103,CVJC2006,CVNM2011,CVNM2101,CVNM2102,CVNM2103,CVNM2104,CVNM2105,CVPB2015,CVPB2101,CVPB2102,CVPB2103,CVPB2104,CVRE2009,CVRE2011,CVRE2013,CVRE2101,CVRE2102,CVRE2103,CVRE2104,CVT,D2D,DAG,DAH,DAT,DBC,DBD,DBT,DC4,DCC,DCL,DCM,DGC,DGW,DHA,DHC,DHG,DHM,DIG,DLG,DMC,DPG,DPM,DPR,DQC,DRC,DRH,DRL,DSN,DTA,DTL,DTT,DVD,DVP,DXG,DXV,E1VFVN30,EIB,ELC,EMC,EVE,EVG,FBT,FCM,FCN,FDC,FIR,FIT,FLC,FMC,FPC,FPT,FRT,FTM,FTS,FUCTVGF1,FUCTVGF2,FUCVREIT,FUEMAV30,FUESSV30,FUESSV50,FUESSVFL,FUEVFVND,FUEVN100,GAB,GAS,GDT,GEG,GEX,GIL,GMC,GMD,GSP,GTA,GTN,GVR,HAG,HAH,HAI,HAR,HAS,HAX,HBC,HCD,HCM,HDB,HDC,HDG,HHP,HHS,HID,HII,HMC,HNG,HOT,HPG,HPX,HQC,HRC,HSG,HSL,HT1,HT2,HTI,HTL,HTN,HTV,HU1,HU3,HUB,HVH,HVN,HVX,IBC,ICT,IDI,IJC,ILB,IMP,ITA,ITC,ITD,JVC,KBC,KDC,KDH,KHP,KMR,KOS,KPF,KSB,L10,LBM,LCG,LCM,LDG,LEC,LGC,LGL,LHG,LIX,LM8,LPB,LSS,MAFPF1,MBB,MCG,MCP,MCV,MDG,MHC,MIG,MSB,MSH,MSN,MWG,NAF,NAV,NBB,NCT,NHA,NHH,NHS,NHW,NKD,NKG,NLG,NNC,NT2,NTL,NVL,NVN,NVT,OCB,OGC,OPC,PAC,PC1,PDN,PDR,PET,PGC,PGD,PGI,PHC,PHR,PHT,PIT,PJT,PLP,PLX,PME,PMG,PNC,PNJ,POM,POW,PPC,PRUBF1,PSH,PTB,PTC,PTL,PVD,PVF,PVT,PXI,PXS,QCG,RAL,RDP,REE,RIC,ROS,S4A,SAB,SAM,SAV,SBA,SBC,SBT,SBV,SC5,SCD,SCR,SCS,SEC,SFC,SFG,SFI,SGN,SGR,SGT,SHA,SHI,SHP,SII,SJD,SJF,SJS,SKG,SMA,SMB,SMC,SPM,SRC,SRF,SSB,SSI,ST8,STB,STG,STK,SVC,SVD,SVI,SVT,SZC,SZL,TAC,TBC,TCB,TCD,TCH,TCL,TCM,TCO,TCR,TCT,TDC,TDG,TDH,TDM,TDP,TDW,TEG,TGG,THG,TIC,TIP,TIX,TLD,TLG,TLH,TMP,TMS,TMT,TN1,TNA,TNC,TNH,TNI,TNT,TPB,TPC,TRA,TRC,TRI,TS4,TSC,TTA,TTB,TTE,TTF,TV2,TVS,TVT,TYA,UDC,UIC,VAF,VCA,VCB,VCF,VCG,VCI,VDP,VDS,VFMVF1,VFMVF4,VFMVFA,VFMVN30,VGC,VHC,VHM,VIB,VIC,VIC11501,VIC11504,VID,VIP,VIS,VIX,VJC,VMD,VNE,VNG,VNL,VNM,VNS,VOS,VPB,VPD,VPG,VPH,VPI,VPL,VPS,VRC,VRE,VSC,VSH,VSI,VTB,VTF,VTO,YBM,YEG,A32,AAS,ABB,ABC,ABI,ABR,AC4,ACE,ACG,ACS,ACV,ADP,AFC,AFX,AG1,AGF,AGP,AGX,AIC,ALV,AMP,AMS,ANT,APF,APL,APT,AQN,ASA,ASD,ATA,ATB,ATD,ATG,AUM,AVC,AVF,B82,BAL,BAM,BBH,BBM,BBT,BCB,BCP,BCV,BDC,BDF,BDG,BDT,BDW,BEL,BGW,BHA,BHC,BHG,BHK,BHP,BHT,BHV,BIO,BKH,BLI,BLN,BLT,BLU,BLW,BM9,BMD,BMF,BMG,BMJ,BMN,BMS,BMV,BNW,BOT,BPW,BQB,BRR,BRS,BSA,BSD,BSG,BSH,BSL,BSP,BSQ,BSR,BT1,BT6,BTB,BTC,BTD,BTG,BTH,BTN,BTR,BTU,BTV,BUD,BVB,BVG,BVL,BVN,BWA,BWS,BXD,BXT,C12,C21,C22,C36,C4G,C71,CAB,CAD,CAM,CAT,CBC,CBI,CBS,CC1,CC4,CCA,CCH,CCM,CCP,CCR,CCT,CCV,CDG,CDH,CDO,CDP,CDR,CE1,CEC,CEG,CEN,CER,CFC,CFM,CFV,CGL,CGP,CGV,CH5,CHC,CHS,CI5,CID,CIP,CK8,CKA,CKD,CKH,CLG,CLS,CLX,CMD,CMF,CMI,CMK,CMN,CMP,CMT,CMW,CNC,CNH,CNN,CNT,CPA,CPH,CPI,CPW,CQN,CQT,CSI,CST,CT3,CT5,CT6,CTA,CTN,CTR,CTW,CVC,CVH,CXH,CYC,CZC,D26,DAC,DAP,DAR,DAS,DBH,DBM,DBW,DC1,DCD,DCF,DCG,DCH,DCI,DCR,DCS,DCT,DDH,DDM,DDN,DDV,DFC,DFF,DGT,DHB,DHD,DHN,DIC,DID,DKC,DKH,DKP,DLC,DLD,DLR,DLT,DLV,DM7,DNA,DNB,DND,DNE,DNF,DNH,DNL,DNN,DNR,DNS,DNT,DNW,DNY,DOC,DOP,DP1,DP2,DPD,DPH,DPP,DPS,DRG,DRI,DSC,DSG,DSP,DSS,DSV,DT4,DTB,DTC,DTE,DTG,DTI,DTN,DTP,DTV,DUS,DVC,DVH,DVN,DVW,DWS,DX2,DXD,DXL,E12,E29,EAD,EFI,EIC,EIN,EME,EMG,EMS,EPC,EPH,EVF,FBA,FBC,FCC,FCS,FDG,FGL,FHN,FHS,FIC,FOC,FOX,FRC,FRM,FSC,FSO,FT1,FTI,G20,G36,GCB,GE2,GER,GGG,GGS,GH3,GHC,GLC,GLW,GND,GQN,GSM,GTC,GTD,GTH,GTK,GTS,GTT,GVT,H11,HAB,HAC,HAF,HAM,HAN,HAV,HAW,HBD,HBH,HBI,HBW,HC1,HC3,HCB,HCI,HCS,HD2,HD3,HD6,HD8,HDM,HDO,HDP,HDW,HEC,HEJ,HEM,HEP,HES,HFB,HFC,HFS,HFT,HFX,HGA,HGC,HGR,HGT,HGW,HHA,HHN,HHR,HHV,HIG,HIZ,HJC,HKB,HKC,HKP,HLA,HLB,HLE,HLG,HLR,HLS,HLT,HLY,HMG,HMS,HNA,HNB,HND,HNE,HNF,HNI,HNP,HNR,HNT,HPB,HPD,HPH,HPI,HPL,HPP,HPT,HPU,HPW,HRB,HRG,HRT,HSA,HSI,HSM,HSP,HSV,HTE,HTG,HTH,HTK,HTM,HTR,HTT,HTU,HTW,HU4,HU6,HUG,HUX,HVA,HVC,HVG,HWS,I10,IBD,IBN,ICC,ICF,ICI,ICN,IDN,IDP,IFC,IFS,IHK,IKH,ILA,ILC,ILS,IME,IMT,IN4,IPA,IPH,IRC,ISG,ISH,IST,ITS,JOS,JSC,KAC,KBE,KCB,KCE,KDF,KGM,KGU,KHA,KHB,KHD,KHL,KHW,KIP,KLB,KLM,KSA,KSC,KSE,KSH,KSK,KSS,KSV,KTB,KTC,KTL,KTU,L12,L44,L45,L63,LAI,LAW,LBC,LCC,LCW,LDW,LG9,LGM,LIC,LKW,LLM,LM3,LMC,LMH,LMI,LNC,LO5,LPT,LQN,LTC,LTG,LWS,LYF,M10,MA1,MBN,MC3,MCH,MCI,MCK,MCM,MCT,MDA,MDF,MDN,MDT,MEC,MEF,MEG,MES,MFS,MGC,MGG,MH3,MHP,MHY,MIC,MIE,MJC,MKP,MKT,MLC,MLN,MLS,MMC,MML,MNB,MND,MPC,MPT,MPY,MQB,MQN,MRF,MSR,MTA,MTB,MTC,MTG,MTH,MTL,MTM,MTP,MTS,MTV,MVC,MVN,MVY,MXC,NAB,NAC,NAS,NAU,NAW,NBE,NBR,NBS,NBT,NCP,NCS,ND2,NDC,NDF,NDP,NDT,NDW,NED,NGC,NHN,NHP,NHT,NHV,NJC,NLS,NMK,NNB,NNG,NNQ,NNT,NOS,NPH,NPS,NQB,NQN,NQT,NS2,NS3,NSG,NSL,NSP,NSS,NTB,NTC,NTF,NTR,NTT,NTW,NUE,NVP,NWT,OIL,OLC,ONW,ORS,PAI,PAP,PAS,PBC,PBK,PBT,PCC,PCF,PCM,PCN,PDT,PDV,PEC,PEG,PEQ,PFL,PFV,PGB,PGV,PHH,PHS,PID,PIS,PIV,PJS,PKR,PLA,PLE,PLO,PMJ,PMT,PMW,PND,PNG,PNP,PNT,POB,POS,POV,PPG,PPH,PPI,PQN,PRO,PRT,PSB,PSG,PSL,PSN,PSP,PTE,PTG,PTH,PTK,PTM,PTO,PTP,PTT,PTV,PTX,PVA,PVE,PVH,PVM,PVO,PVP,PVR,PVV,PVX,PVY,PWA,PWS,PX1,PXA,PXC,PXL,PXM,PXT,PYU,QBR,QCC,QHW,QLD,QLT,QNC,QNS,QNT,QNU,QNW,QPH,QSP,QTP,RAT,RBC,RCC,RCD,REM,RGC,RHN,RLC,RTB,RTH,RTS,S12,S27,S33,S72,S74,S96,SAC,SAL,SAP,SAS,SB1,SBD,SBH,SBL,SBM,SBR,SBS,SCA,SCC,SCG,SCH,SCJ,SCL,SCO,SCV,SCY,SD1,SD3,SD7,SD8,SDB,SDD,SDE,SDF,SDH,SDI,SDJ,SDK,SDP,SDV,SDX,SDY,SEA,SEP,SFT,SGB,SGO,SGP,SGS,SHC,SHG,SHV,SHX,SID,SIG,SIP,SIV,SJC,SJG,SJM,SKH,SKN,SKV,SLC,SNC,SNZ,SON,SOV,SP2,SPA,SPB,SPC,SPD,SPH,SPP,SPV,SQC,SRB,SRT,SSF,SSG,SSH,SSN,SST,SSU,STD,STH,STL,STS,STT,STU,STV,STW,SUM,SVG,SVH,SVL,SWC,SZE,T12,TA3,TA6,TAG,TAN,TAP,TAW,TB8,TBD,TBN,TBR,TBT,TCI,TCJ,TCK,TCW,TDA,TDB,TDF,TDS,TEC,TEL,TGP,TH1,THN,THP,THR,THU,THW,TID,TIE,TIS,TKA,TKG,TL4,TLI,TLP,TLT,TMG,TMW,TNB,TND,TNM,TNP,TNS,TNW,TNY,TOP,TOT,TOW,TPS,TQN,TQW,TR1,TRS,TRT,TS3,TS5,TSD,TSG,TSJ,TTD,TTG,TTJ,TTN,TTP,TTR,TTS,TTV,TUG,TV1,TV6,TVA,TVG,TVH,TVM,TVN,TVP,TVU,TVW,TW3,UCT,UDJ,UDL,UEM,UMC,UPC,UPH,USC,USD,V11,V15,VAB,VAV,VBB,VBG,VBH,VC5,VCE,VCGPVF,VCP,VCR,VCT,VCW,VCX,VDB,VDM,VDN,VDT,VE9,VEA,VEC,VECX,VEE,VEF,VES,VET,VFC,VFR,VFS,VGG,VGI,VGL,VGR,VGT,VGV,VHD,VHF,VHG,VHH,VHI,VIA,VIH,VIM,VIN,VIR,VIW,VKD,VKP,VLB,VLC,VLF,VLG,VLP,VLW,VMA,VMG,VMI,VNA,VNB,VNH,VNI,VNN,VNP,VNX,VNY,VOC,VPA,VPC,VPK,VPR,VPW,VQC,VRG,VSE,VSF,VSG,VSN,VSP,VST,VT1,VT8,VTA,VTD,VTE,VTG,VTI,VTK,VTM,VTP,VTQ,VTR,VTS,VTX,VVN,VW3,VWS,VXP,VXT,WSB,WTC,WTN,X18,X26,X77,XDH,XHC,XLV,XMC,XMD,XPH,YBC,YRC,YTC"
    # list_symbol_string = "MSB"

    if len(sys.argv) > 1 and os_name != 'Windows':
        # print(sys.argv)
        # print("run args")
        send_message_tele("==============Test upcode=======================")
        list_symbol_string = 'CTR,TNG,NTL,NLG,VHM,PNJ,VHC,DIG,DPR,IDC,SZC,KBC,HCM,MSB,PC1,BMI,HPG'
        if(sys.argv[1] == 'account'):
            check_account(beauty_print)
        if(sys.argv[1] == 'buy'):
            check_buy_bot(beautify_list_rated_symbol,list_symbol_string)
        send_message_tele("==============Ket thuc Test upcode==============")
    elif len(sys.argv) > 1 and os_name == 'Windows':
        check_buy_bot(beautify_list_rated_symbol,list_symbol_string)
    else :
        if os_name == 'Windows':
            check_account(beauty_print)
        else:
            check_buy_bot(beautify_list_rated_symbol,list_symbol_string)
    