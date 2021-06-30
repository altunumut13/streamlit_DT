http_transfer = """/****** Script for SelectTopNRows command from SSMS  ******/

SET ANSI_WARNINGS OFF
select HTTPO2.CollectionName,HTTPO2.ASideFileName,HTTPO2.PosId,HTTPO2.longitude,HTTPO2.latitude,HTTPO2.typeoftest,HTTPO2.Protocol,
HTTPO2.Operation,
HTTPO2.startTime,
round(convert(float,HTTPO2.duration*1.00/1000),2) as 'Duration(sec)',
sum(HTTPO2.[LTE 3CA(%)]) as 'LTE 3CA%',
sum(HTTPO2.[LTE 2CA(%)]) as 'LTE 2CA%',
sum(HTTPO2.[LTE(%)]) as 'LTE %',
sum(HTTPO2.[DC-HSPA+(%)]) as 'DC-HSDPA%',
sum(HTTPO2.[HSPA+ or Less(%)]) as 'HSPA+ or Less%',
HTTPO2.[Throughput(Kbps)] as 'Throughput(kbps)',
round(convert(float,HTTPO2.RSRP),0) as RSRP,
round(convert(float,HTTPO2.RSRQ),0) as RSRQ,
round(convert(float,HTTPO2.SINR),0) as SINR,
HTTPO2.qualityIndication,
HTTPO2.RemoteFilename
into #tmp1
from(select filelist.CollectionName,filelist.ASideFileName,position.PosId,Position.longitude,Position.latitude,DwDataTechnology.DataTechnologyReporting,
sum(DwDataTechnology.Duration) AS 'TechDuration',
TestInfo.duration,
case when DwDataTechnology.DataTechnologyReporting= 'LTE' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'LTE(%)',
case when DwDataTechnology.DataTechnologyReporting= 'LTE 2CCA' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'LTE 2CA(%)',
case when DwDataTechnology.DataTechnologyReporting= 'LTE 3CCA' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'LTE 3CA(%)',
case when DwDataTechnology.DataTechnologyReporting= 'DC-HSPA+' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'DC-HSPA+(%)',
case when DwDataTechnology.DataTechnologyReporting not like '%LTE%' and DwDataTechnology.DataTechnologyReporting not like '%DC%' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'HSPA+ or Less(%)',
Round(convert(float,ResultsHTTPTransferTest.BytesTransferred*8.00/ResultsHTTPTransferTest.Duration),2) AS 'Throughput(Kbps)',
TestInfo.qualityIndication,
TestInfo.typeoftest,
testinfo.startTime,
ResultsHTTPTransferParameters.Protocol,
ResultsHTTPTransferParameters.Operation,
ResultsHTTPTransferParameters.RemoteFilename,
avg(LTEMeasurementReport.RSRP) as RSRP,
avg(LTEMeasurementReport.RSRQ) as RSRQ,
avg(LTEMeasurementReport.SINR0) as SINR
from ResultsHTTPTransferParameters,sessions,FileList,DataSession,Position,TestInfo
right join LTEMeasurementReport on LTEMeasurementReport .TestId=TestInfo.TestId
right join DwDataTechnology on TestInfo.TestId=DwDataTechnology.TestId
left join ResultsHTTPTransferTest on TestInfo.TestId = ResultsHTTPTransferTest.TestId and ResultsHTTPTransferTest.LastBlock=1
where ResultsHTTPTransferParameters.TestId = testinfo.TestId and sessions.SessionId=TestInfo.SessionId and DataSession.SessionId=Sessions.SessionId and FileList.FileId=Sessions.FileId
and position.PosId=ResultsHTTPTransferTest.PosId
group by filelist.CollectionName,filelist.ASideFileName,position.PosId,Position.longitude,Position.latitude,ResultsHTTPTransferTest.BytesTransferred,ResultsHTTPTransferTest.Duration,
DwDataTechnology.DataTechnologyReporting,
TestInfo.duration,
TestInfo.qualityIndication,
TestInfo.typeoftest,
testinfo.startTime,
testinfo.TestName,
ResultsHTTPTransferParameters.Protocol,
ResultsHTTPTransferParameters.Operation,
ResultsHTTPTransferParameters.Host,
ResultsHTTPTransferParameters.LocalFilename,
ResultsHTTPTransferParameters.RemoteFilename,DwDataTechnology.Duration
) HTTPO2
where HTTPO2.qualityIndication is NULL or HTTPO2.qualityIndication like '%error%'
group by HTTPO2.CollectionName,HTTPO2.ASideFileName,HTTPO2.longitude,HTTPO2.latitude,HTTPO2.duration,
HTTPO2.startTime,HTTPO2.qualityIndication,HTTPO2.PosId,
HTTPO2.typeoftest,
HTTPO2.startTime,
HTTPO2.Protocol,
HTTPO2.Operation,
HTTPO2.RemoteFilename,HTTPO2.[Throughput(Kbps)],HTTPO2.RSRP,
HTTPO2.RSRQ,
HTTPO2.SINR
order by HTTPO2.startTime

select DmnGeographicRegion.Country,DmnGeographicRegion.Province,position.posid,Position.longitude,Position.latitude
into #tmp2
from DwBinRegionMapping,DmnGeographicRegion,PositionBinRelation,position
where DwBinRegionMapping.DwRegionId=DmnGeographicRegion.DwRegionId and DmnGeographicRegion.ZoomLevel=7
and PositionBinRelation.IdX= DwBinRegionMapping.IdX and PositionBinRelation.IdY= DwBinRegionMapping.IdY and Position.PosId=PositionBinRelation.PosId

select
t1.CollectionName,
t1.ASideFileName,
t2.Country,
t2.Province,
t1.longitude,
t1.latitude,
t1.startTime,
t1.typeoftest,
t1.Operation,
t1.Protocol,
t1.[Duration(sec)] as 'Duration',
t1.qualityIndication,
t1.RSRP,
t1.RSRQ,
t1.SINR,
t1.RemoteFilename,
t1.[Throughput(kbps)] as 'Throughput',
t1.[LTE 3CA%] as 'LTE 3CA%',
t1.[LTE 2CA%] as 'LTE 2CA%',
t1.[LTE %] as 'LTE%',
t1.[DC-HSDPA%] as  'DC-HSPA&',
t1.[HSPA+ or Less%] as 'HSPA+ or Less%'

from #tmp1 t1 left outer join #tmp2 t2 on t1.PosId=t2.PosId
drop table #tmp1
drop table #tmp2"""


ROUTE = """SELECT distinct latitude,longitude from position where Distance <> 0 """

deneme = """SELECT TOP 100 * from Position"""

data_fail_types ="""/****** Script for SelectTopNRows command from SSMS  ******/
select case when RSRP < -105 then 'RF-Related Fail' else 'Non-RF Related Fail'end as FailType,
latitude,
longitude
FROM(

select HTTPO2.TestId,
sum(HTTPO2.[LTE 3CA(%)]) as 'LTE 3CA%',
sum(HTTPO2.[LTE 2CA(%)]) as 'LTE 2CA%',
sum(HTTPO2.[LTE(%)]) as 'LTE %',
sum(HTTPO2.[DC-HSPA+(%)]) as 'DC-HSDPA%',
sum(HTTPO2.[HSPA+ or Less(%)]) as 'HSPA+ or Less%',
HTTPO2.[Throughput(Kbps)] as 'Throughput(kbps)',
round(convert(float,HTTPO2.RSRP),0) as RSRP,
round(convert(float,HTTPO2.RSRQ),0) as RSRQ,
round(convert(float,HTTPO2.SINR),0) as SINR,
HTTPO2.qualityIndication,
HTTPO2.typeoftest,
HTTPO2.startTime,
HTTPO2.Protocol,
HTTPO2.Operation,
HTTPO2.RemoteFilename,
HTTPO2.PosId
from(select testinfo.testid,DwDataTechnology.DataTechnologyReporting,testinfo.PosId,
sum(DwDataTechnology.Duration) AS 'TechDuration',
TestInfo.duration,
case when DwDataTechnology.DataTechnologyReporting= 'LTE' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'LTE(%)',
case when DwDataTechnology.DataTechnologyReporting= 'LTE 2CCA' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'LTE 2CA(%)',
case when DwDataTechnology.DataTechnologyReporting= 'LTE 3CCA' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'LTE 3CA(%)',
case when DwDataTechnology.DataTechnologyReporting= 'DC-HSPA+' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'DC-HSPA+(%)',
case when DwDataTechnology.DataTechnologyReporting not like '%LTE%' and DwDataTechnology.DataTechnologyReporting not like '%DC%' then round(convert(float,DwDataTechnology.Duration*100.0/TestInfo.duration),1) else NULL end as 'HSPA+ or Less(%)',
Round(convert(float,ResultsHTTPTransferTest.BytesTransferred*8.00/ResultsHTTPTransferTest.Duration),2) AS 'Throughput(Kbps)',
TestInfo.qualityIndication,
TestInfo.typeoftest,
testinfo.startTime,
ResultsHTTPTransferParameters.Protocol,
ResultsHTTPTransferParameters.Operation,
ResultsHTTPTransferParameters.RemoteFilename,
avg(LTEMeasurementReport.RSRP) as RSRP,
avg(LTEMeasurementReport.RSRQ) as RSRQ,
avg(LTEMeasurementReport.SINR0) as SINR
from ResultsHTTPTransferParameters,sessions,DataSession,TestInfo
right join LTEMeasurementReport on LTEMeasurementReport .TestId=TestInfo.TestId
right join DwDataTechnology on TestInfo.TestId=DwDataTechnology.TestId
left join ResultsHTTPTransferTest on TestInfo.TestId = ResultsHTTPTransferTest.TestId and ResultsHTTPTransferTest.LastBlock=1
where ResultsHTTPTransferParameters.TestId = testinfo.TestId and sessions.SessionId=TestInfo.SessionId and DataSession.SessionId=Sessions.SessionId
group by testinfo.testid,ResultsHTTPTransferTest.BytesTransferred,ResultsHTTPTransferTest.Duration,
DwDataTechnology.DataTechnologyReporting,
testinfo.PosId,
TestInfo.duration,
TestInfo.qualityIndication,
TestInfo.typeoftest,
testinfo.startTime,
testinfo.TestName,
ResultsHTTPTransferParameters.Protocol,
ResultsHTTPTransferParameters.Operation,
ResultsHTTPTransferParameters.Host,
ResultsHTTPTransferParameters.LocalFilename,
ResultsHTTPTransferParameters.RemoteFilename,DwDataTechnology.Duration
) HTTPO2
where HTTPO2.qualityIndication is NULL or HTTPO2.qualityIndication like '%error%'
group by HTTPO2.TestId,
HTTPO2.startTime,HTTPO2.qualityIndication,
HTTPO2.typeoftest,
HTTPO2.Protocol,
HTTPO2.Operation,
HTTPO2.RemoteFilename,HTTPO2.[Throughput(Kbps)],HTTPO2.RSRP,
HTTPO2.RSRQ,
HTTPO2.SINR,
HTTPO2.PosId
) as temp_df ,position

where temp_df.PosId = position.PosId
"""
