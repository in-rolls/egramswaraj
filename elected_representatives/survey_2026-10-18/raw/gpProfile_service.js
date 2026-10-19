gpProfileModule.service('gpProfileService', [ '$http', function($http) {
	
  var service = {};
 
  service.findStateWise = function(year) {
	  return $http.get("gpProfileStateReport.do?year="+year,{});
  };
  service.findDistrictCountForGP = function(stateId, year) {
	  return $http.get("gpProfileZpReport.do?stateId="+stateId+"&year="+year,{});
  };
  service.findBlockCountForGP = function(stateId, code, year) {
	  return $http.get("gpProfileBpReport.do?stateId="+stateId+"&code="+code+"&year="+year,{});
  };
  service.findVillageWise = function(stateId, code, year) {
	  return $http.get("gpProfileGpReport.do?stateId="+stateId+"&code="+code+"&year="+year,{});
  };
  return service;

} ]);


