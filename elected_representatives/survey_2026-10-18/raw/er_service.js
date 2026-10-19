ElectedModule.service('ElectedService', [ '$http', function($http) {
	
  var service = {};
 
  service.findStateWise = function(year) {
	  return $http.get("ElectedStateReport.do?year="+year,{});
  };
  service.findDistrictCountForGP = function(stateId, year) {
	  return $http.get("ElectedZpReport.do?stateId="+stateId+"&year="+year,{});
  };
  service.findBlockCountForGP = function(stateId, code, year) {
	  return $http.get("ElectedBpReport.do?stateId="+stateId+"&code="+code+"&year="+year,{});
  };
  service.findVillageWise = function(stateId, code, year) {
	  return $http.get("ElectedGpReport.do?stateId="+stateId+"&code="+code+"&year="+year,{});
  };
   
  service.findElectedDetail = function(code,stateCode,level) {
	  return $http.get("ElectedMemberRepresent.do?code="+code+"&stateCode="+stateCode+"&level="+level,{});
  };
  
  /** *********************************/
  service.findStateWiseZp = function(year) {
	  return $http.get("ElectedStateReportZp.do?year="+year,{});
  };
  
  service.findStateWiseBp = function(year) {
	  return $http.get("ElectedStateReportBp.do?year="+year,{});
  };
  
  service.findStateWiseGp = function(year) {
	  return $http.get("ElectedStateReportGp.do?year="+year,{});
  };
  
  service.findPanchayatByStateCode = function(stateCode, year, templateId) {
		if(templateId=='zpTemplate'){
			return $http.get("ElectedStatePanReport.do?stateCode="+stateCode+"&year="+year,{});
		}else if(templateId=='bpTemplate'){
			return $http.get("ElectedStateZpWiseBpCount.do?stateCode="+stateCode+"&year="+year,{});
		}else if(templateId=='gpTemplate'){
			return $http.get("ElectedStatePanReportGp.do?stateCode="+stateCode+"&year="+year,{});
		}
	  
  };
  service.findBpByZpCode = function(stateCode, year, templateId, zpCode) {
		if(templateId=='zpTemplate'){
			return $http.get("ElectedStatePanReport.do?stateCode="+stateCode+"&year="+year,{});
		}else if(templateId=='bpTemplate'){
			return $http.get("findElectedStateBpByZpCode.do?stateCode="+stateCode+"&year="+year+"&zpCode="+zpCode,{});
		}else if(templateId=='gpTemplate'){
			return $http.get("ElectedStatePanReportGp.do?stateCode="+stateCode+"&year="+year,{});
		}
	  
	};
	service.findBpNameAndGPCountByZpCode = function(stateCode, year, zpCode) {
		return $http.get("findBpNameAndGPCountByZpCode.do?stateCode="+stateCode+"&year="+year+"&zpCode="+zpCode,{});
	};

	service.findBpGpNameBErCountBpCode = function(stateCode, year, bpCode, object, templateId) {
		if([30, 38, 12, 11, 34, 31].includes(object.stateCode) && templateId=='gpTemplate'){
			return $http.get("findGpNameAndERCountByBpCode.do?stateCode="+stateCode+"&year="+year+"&bpCode="+object.zpCode,{});
		}else if([13, 15].includes(object.stateCode) && templateId=='gpTemplate'){
			return $http.get("findGpNameAndERCountByBpCode.do?stateCode="+stateCode+"&year="+year+"&bpCode="+bpCode,{});
		}else{
			return $http.get("findGpNameAndERCountByBpCode.do?stateCode="+stateCode+"&year="+year+"&bpCode="+bpCode,{});	
		}
	
	};
	
  return service;

} ]);


