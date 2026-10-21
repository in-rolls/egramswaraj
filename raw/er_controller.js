var ElectedModule = angular.module("ElectedModule", []);
ElectedModule.controller("ElectedController", [ '$scope', "ElectedService", function($scope, ElectedService) {
	document.getElementById('displayStateWise').style.display = 'none';
	if(document.getElementById('displayBpWiseZp')){
		document.getElementById('displayBpWiseZp').style.display = 'none';
	}
	if(document.getElementById('districtCountLevel')){
		document.getElementById('districtCountLevel').style.display = 'none';
	}
	if(document.getElementById('villageLevel')){
		document.getElementById('villageLevel').style.display = 'none';
	}
	$scope.stateCode = null;
	$scope.stateName = null;
	$scope.districtId = null;
	$scope.districtName = null;
	$scope.zpName = null;
	$scope.bpName = null;
	$scope.gpName = null;
	$scope.zpCode = null;
	$scope.bpCode = null;
	$scope.code = null;
	$scope.villcd =null;
	$scope.name = null;
	$scope.typeflg = null;
	$scope.type = 'S';
	$scope.loader = true;
	$scope.loaderGp = true;
	$scope.details = {};
	$scope.objectDetails = null;
	$scope.zpViewTemplateId = null;
	$scope.bpViewTemplateId = null;
	$scope.gpViewTemplateId = null;
	$scope.year = $("#year").val();
	

	// By Pradeep
	//var currentYear = new Date().getFullYear();
	var currentYear = $scope.year.split('-')[0];
	
	ElectedService.findStateWiseZp(currentYear).then(function(response) {
		
		$scope.loader = true;
		$scope.type = 'S';
		$scope.data = response.data;
		$scope.detailsZp = {};
		$scope.sumTotalCountZp = 0;
		$scope.totalERCountZp = 0;
		$scope.totalMaleCountZp = 0;
		$scope.totalFemaleCountZp = 0;
		$scope.totalOtherCountZp = 0;
		
		$scope.sumTotalCountZpBack = 0;
		$scope.totalERCountZpBack = 0;
		$scope.totalMaleCountZpBack = 0;
		$scope.totalFemaleCountZpBack = 0;
		$scope.totalOtherCountZpBack = 0;
		
		
		if (response.data) {
            $scope.detailsZp=response.data;
            angular.forEach($scope.detailsZp, function(obj, key) {
    			if(obj.stateCode) {
    				$scope.sumTotalCountZp = $scope.sumTotalCountZp + obj.zpCount;
    				$scope.totalERCountZp = $scope.totalERCountZp + obj.zperCount;
    				$scope.totalMaleCountZp = $scope.totalMaleCountZp + obj.maleCount;
    				$scope.totalFemaleCountZp = $scope.totalFemaleCountZp + obj.femaleCount;
    				$scope.totalOtherCountZp = $scope.totalOtherCountZp + obj.otherCount;
    				
    				$scope.sumTotalCountZpBack = $scope.sumTotalCountZpBack + obj.zpCount;
    				$scope.totalERCountZpBack = $scope.totalERCountZpBack + obj.zperCount;
    				$scope.totalMaleCountZpBack = $scope.totalMaleCountZpBack + obj.maleCount;
    				$scope.totalFemaleCountZpBack = $scope.totalFemaleCountZpBack + obj.femaleCount;
    				$scope.totalOtherCountZpBack = $scope.totalOtherCountZpBack + obj.otherCount;
    				
    			}
    			
    		});
        } else {
            console.error("No data received from the API!");
        }
		
		$scope.loader = false;
    });
	

	ElectedService.findStateWiseBp(currentYear).then(function(response) {

		$scope.loader = true;
		$scope.type = 'S';
	
		$scope.detailsBp = {};
		$scope.sumTotalCountBpBack = 0;
		$scope.totalERCountBpBack = 0;
		$scope.totalMaleCountBpBack = 0;
		$scope.totalFemaleCountBpBack = 0;
		$scope.totalOtherCountBpBack = 0;
		
		$scope.sumTotalCountBp = 0;
		$scope.totalERCountBp = 0;
		$scope.totalMaleCountBp = 0;
		$scope.totalFemaleCountBp = 0;
		$scope.totalOtherCountBp = 0;
		
		if (response.data) {
		
            $scope.detailsBp=response.data;
            angular.forEach($scope.detailsBp, function(obj, key) {
    	
    			if(obj.stateCode) {
    				
    				$scope.sumTotalCountBp = $scope.sumTotalCountBp + obj.bpCount;
    				$scope.totalERCountBp = $scope.totalERCountBp+ obj.bperCount;
    				$scope.totalMaleCountBp = $scope.totalMaleCountBp + obj.maleCount;
    				$scope.totalFemaleCountBp = $scope.totalFemaleCountBp + obj.femaleCount;
    				$scope.totalOtherCountBp = $scope.totalOtherCountBp + obj.otherCount;
    				
    				$scope.sumTotalCountBpBack = $scope.sumTotalCountBpBack + obj.bpCount;
    				$scope.totalERCountBpBack = $scope.totalERCountBpBack + obj.bperCount;
    				$scope.totalMaleCountBpBack = $scope.totalMaleCountBpBack + obj.maleCount;
    				$scope.totalFemaleCountBpBack = $scope.totalFemaleCountBpBack + obj.femaleCount;
    				$scope.totalOtherCountBpBack = $scope.totalOtherCountBpBack + obj.otherCount;
    				
    			}
    			
    		});
        } else {
            console.error("No data received from the API!");
        }
		

		$scope.loader = false;
    });
	

	ElectedService.findStateWiseGp(currentYear).then(function(response) {
		$scope.loader = true;
		$scope.loaderGp = true;
		$scope.type = 'S';
		
		$scope.detailsGp = {};
		$scope.sumTotalCountGp = 0;
		$scope.totalERCountGp = 0;
		$scope.totalMaleCountGp = 0;
		$scope.totalFemaleCountGp = 0;
		$scope.totalOtherCountGp = 0;
		
		$scope.sumTotalCountGpBack = 0;
		$scope.totalERCountGpBack = 0;
		$scope.totalMaleCountGpBack = 0;
		$scope.totalFemaleCountGpBack = 0;
		$scope.totalOtherCountGpBack = 0;
		
		if (response.data) {
		
            $scope.detailsGp=response.data;
            angular.forEach($scope.detailsGp, function(obj, key) {
    	
    			if(obj.stateCode) {
    				
    				$scope.sumTotalCountGp = $scope.sumTotalCountGp + obj.gpCount;
    				$scope.totalERCountGp =  $scope.totalERCountGp + obj.gperCount;
    				$scope.totalMaleCountGp = $scope.totalMaleCountGp + obj.maleCount;
    				$scope.totalFemaleCountGp = $scope.totalFemaleCountGp + obj.femaleCount;
    				$scope.totalOtherCountGp = $scope.totalOtherCountGp + obj.otherCount;
    				
    				$scope.sumTotalCountGpBack = $scope.sumTotalCountGpBack + obj.gpCount;
    				$scope.totalERCountGpBack =  $scope.totalERCountGpBack + obj.gperCount;
    				$scope.totalMaleCountGpBack = $scope.totalMaleCountGpBack + obj.maleCount;
    				$scope.totalFemaleCountGpBack = $scope.totalFemaleCountGpBack + obj.femaleCount;
    				$scope.totalOtherCountGpBack = $scope.totalOtherCountGpBack + obj.otherCount;
    				
    			}
    			
    		});
        } else {
            console.error("No data received from the API!");
        }
		$scope.loaderGp = false;
		$scope.loader = false;
    });
	
	
	// drilthru click on state name, etc
	
	$scope.onViewPanchayatList = function onViewPanchayatList(stateId, stateName, templateId, viewTemplateId){
		$scope.type = '';
		$scope.loader = true;
		document.getElementById('stateLevel').style.display = 'none';	
		document.getElementById('displayStateWise').style.display = '';
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = 'none';
		}
		if(document.getElementById('villageLevel')){
			document.getElementById('villageLevel').style.display = 'none';
		}
		if(document.getElementById('districtCountLevel')){
			document.getElementById('districtCountLevel').style.display = 'none';
		}
		$scope.stateCode = stateId;
		$scope.stateName = stateName;
		if(templateId=='zpTemplate'){
			$scope.zpViewTemplateId = viewTemplateId;
		}else if(templateId=='bpTemplate'){
			$scope.bpViewTemplateId = viewTemplateId;
		}else if(templateId=='gpTemplate'){
			$scope.gpViewTemplateId = viewTemplateId;
		}
		/*if(stateId==35 && templateId=='bpTemplate'){
			if(document.getElementById('displayBpWiseZp')){
				document.getElementById('displayBpWiseZp').style.display = '';
			}
			if(document.getElementById('displayStateWise')){
				document.getElementById('displayStateWise').style.display = 'none';
			}
			const obj={
				zpCode: 111,
				stateName: stateName
			}
			onViewBptListData(stateId, currentYear, templateId, obj);
		}
		else */
		if((stateId==13|| stateId==15) && templateId=='gpTemplate'){
			const obj={
					stateCode: stateId,
					stateName : stateName,
					zpName : "",
					bpName : "",
					bpCode : "000"
			}
			$scope.onBpGpNameBErCount(obj, 'gpTemplate', 2);
		}else{
			onViewPanchayatListData(stateId, currentYear, templateId, stateName);
		}
		
	}
	
	function onViewPanchayatListData(stateId, currentYear, templateId, stateName){
		   
		$scope.loader = true;
		$scope.type = 'B';
	
		$scope.detailsData = {};
		$scope.sumTotalZpCount = 0;
		$scope.totalERCount = 0;
		$scope.sumTotalCountGp = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;

		// GP
		$scope.totalGPsInState = 0;
		
		ElectedService.findPanchayatByStateCode(stateId, currentYear, templateId).then(function(response) {
			if (response.data){
				$scope.data = response.data;
				$scope.detailsData = response.data;
				 angular.forEach($scope.detailsData, function(obj, key) {
	    			if(obj.zpCode) {
	    				obj.stateName=stateName;
	    				
	    				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
	    				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
	    				$scope.totalOtherCount = $scope.totalOtherCount + obj.otherCount;
	    				
	    				if(templateId=='zpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.zperCount;
	    				}else if(templateId=='bpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.bperCount;
	    					$scope.sumTotalZpCount = $scope.sumTotalZpCount + obj.bpCount;
	    					
	    				}else if(templateId=='gpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.gperCount;
	    					$scope.sumTotalCountGp = $scope.sumTotalCountGp + obj.gpCount;
	    				}
	    			}
		    	});
			} else {
	            console.error("No data received from the API!");
	        }
			$scope.loader = false;
	    });
	}
	
	/***************************/
	// GP level
	$scope.onZpBpNameBpCount = function onZpBpNameBpCount(object, templateId, viewTemplateId){
		$scope.type = '';
		$scope.loader = true;
		$scope.stateName = object.stateName;
		$scope.zpName = object.zpName;
		$scope.bpName = object.bpName;
		$scope.objectDetails = object;
		document.getElementById('stateLevel').style.display = 'none';	
		document.getElementById('displayStateWise').style.display = 'none';
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = 'none';
		}
		if(document.getElementById('districtCountLevel')){
			document.getElementById('districtCountLevel').style.display = '';
		}
		if(document.getElementById('villageLevel')){
			document.getElementById('villageLevel').style.display = 'none';
		}
		if(templateId=='zpTemplate'){
			$scope.zpViewTemplateId = viewTemplateId;
		}else if(templateId=='bpTemplate'){
			$scope.bpViewTemplateId = viewTemplateId;
		}else if(templateId=='gpTemplate'){
			$scope.gpViewTemplateId = viewTemplateId;
		}
		$scope.stateCode = object.stateCode;
		$scope.stateName = object.stateName;
		$scope.zpName = object.zpName;
		
		$scope.loader = true;
		$scope.type = 'B';
		$scope.detailsData = {};
		$scope.sumTotalZpCount = 0;
		$scope.totalERCount = 0;
		$scope.sumTotalCountGp = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;

		if(templateId=='gpTemplate' && [30, 38, 12, 11, 34, 31].includes(object.stateCode)){
			$scope.onBpGpNameBErCount(object, 'gpTemplate', 2);
		}else{
			ElectedService.findBpNameAndGPCountByZpCode(object.stateCode, currentYear, object.zpCode).then(function(response) {
				if (response.data){
					$scope.data = response.data;
					$scope.detailsData = response.data;
					 angular.forEach($scope.detailsData, function(obj, key) {
		    			if(obj.bpCode) {
		    				obj.stateName=object.stateName;
		    				obj.zpName=object.zpName;
		    				obj.zpCode = object.zpCode;
		    				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
		    				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
		    				$scope.totalOtherCount = $scope.totalOtherCount + obj.otherCount;
		    				
		    				if(templateId=='zpTemplate'){
		    					$scope.totalERCount = $scope.totalERCount + obj.zperCount;
		    				}else if(templateId=='bpTemplate'){
		    					$scope.totalERCount = $scope.totalERCount + obj.bperCount;
		    					$scope.sumTotalZpCount = $scope.sumTotalZpCount + obj.bpCount;
		    					
		    				}else if(templateId=='gpTemplate'){
		    					$scope.totalERCount = $scope.totalERCount + obj.gperCount;
		    					$scope.sumTotalCountGp = $scope.sumTotalCountGp + obj.gpCount;
		    				}
		    				
		    			}
			    	});
				} else {
		            console.error("No data received from the API!");
		        }
				$scope.loader = false;
		    });
		}
		
		
		
	}
	
	$scope.onBpGpNameBErCount = function onBpGpNameBErCount(object, templateId, viewTemplateId){
		$scope.type = '';
		$scope.loader = true;
		$scope.stateName = object.stateName;
		$scope.zpName = object.zpName;
		$scope.bpName = object.bpName;
		$scope.bpCode = object.bpCode;
		$scope.objectDetails = object;
		document.getElementById('stateLevel').style.display = 'none';	
		document.getElementById('displayStateWise').style.display = 'none';
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = 'none';
		}
		if(document.getElementById('districtCountLevel')){
			document.getElementById('districtCountLevel').style.display = 'none';
		}
		if(document.getElementById('villageLevel')){
			document.getElementById('villageLevel').style.display = '';
		}
		if(templateId=='zpTemplate'){
			$scope.zpViewTemplateId = viewTemplateId;
		}else if(templateId=='bpTemplate'){
			$scope.bpViewTemplateId = viewTemplateId;
		}else if(templateId=='gpTemplate'){
			$scope.gpViewTemplateId = viewTemplateId;
		}
		$scope.stateCode = object.stateCode;
		$scope.stateName = object.stateName;
		$scope.zpName = object.zpName;
		
		$scope.loader = true;
		$scope.type = 'B';
		$scope.detailsData = {};
		$scope.sumTotalZpCount = 0;
		$scope.totalERCount = 0;
		$scope.sumTotalCountGp = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;

		
		ElectedService.findBpGpNameBErCountBpCode(object.stateCode, currentYear, object.bpCode, object, templateId).then(function(response) {
			if (response.data){
				$scope.data = response.data;
				$scope.detailsData = response.data;
				 angular.forEach($scope.detailsData, function(obj, key) {
	    			if(obj.gpCode) {
	    				obj.stateName=object.stateName;
	    				
	    				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
	    				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
	    				$scope.totalOtherCount = $scope.totalOtherCount + obj.otherCount;
	    				
	    				if(templateId=='zpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.zperCount;
	    				}else if(templateId=='bpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.bperCount;
	    					$scope.sumTotalZpCount = $scope.sumTotalZpCount + obj.bpCount;
	    					
	    				}else if(templateId=='gpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.gperCount;
	    				}
	    				
	    				
	    				
	    			}
		    	});
			} else {
	            console.error("No data received from the API!");
	        }
			$scope.loader = false;
	    });
		
	}
	
	/***************************/
	
	
	$scope.onBackButton = function(stateCode, type, zpCode, templateId) {
		document.getElementById('displayStateWise').style.display = 'none';
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = 'none';
		}
		if(document.getElementById('ElectedLevel')){
			document.getElementById('ElectedLevel').style.display = 'none';
		}
		if(document.getElementById('districtCountLevel')){
			document.getElementById('districtCountLevel').style.display = 'none';
		}
		if(document.getElementById('villageLevel')){
			document.getElementById('villageLevel').style.display = 'none';
		}
		document.getElementById('stateLevel').style.display = '';

	
		
		if(templateId=='gpTemplate'){
			$scope.sumTotalCountGp = $scope.sumTotalCountGpBack;
			$scope.totalERCountGp =  $scope.totalERCountGpBack;
			$scope.totalMaleCountGp = $scope.totalMaleCountGpBack;
			$scope.totalFemaleCountGp = $scope.totalFemaleCountGpBack;
			$scope.totalOtherCountGp = $scope.totalOtherCountGpBack;
		}
		if(templateId=='zpTemplate'){
			if($scope.zpViewTemplateId==0){
				$scope.stateName = null;
				$scope.type = 'S';
			}else if($scope.zpViewTemplateId==1){
				$scope.onViewPanchayatList($scope.stateCode, $scope.stateName, 'zpTemplate', 0);
			}else{
				$scope.stateName = null;
				$scope.type = 'S';
			}
			
		}else if(templateId=='bpTemplate'){
			if($scope.bpViewTemplateId==0){
				$scope.stateName = null;
				$scope.type = 'S';
			}else if($scope.bpViewTemplateId==1){
				$scope.onViewPanchayatList($scope.stateCode, $scope.stateName, 'bpTemplate', 0);
			}else if($scope.bpViewTemplateId==2){
				$scope.onClickBpCountOn($scope.stateCode ,'bpTemplate',$scope.objectDetails, 1);
			}else{
				$scope.stateName = null;
				$scope.type = 'S';
			}
		}else if(templateId=='gpTemplate'){
			if($scope.gpViewTemplateId==0){
				$scope.stateName = null;
				$scope.type = 'S';
			}else if($scope.gpViewTemplateId==1){
				$scope.onViewPanchayatList($scope.stateCode, $scope.stateName, 'gpTemplate', 0);
			}else if($scope.gpViewTemplateId==2){
				if([30, 38, 12, 11, 34, 31].includes($scope.stateCode)){
					$scope.onViewPanchayatList($scope.stateCode, $scope.stateName, 'gpTemplate', 0);
//					$scope.onZpBpNameBpCount($scope.objectDetails, 'gpTemplate', 1);
				}else if(($scope.stateCode==13|| $scope.stateCode==15) && templateId=='gpTemplate'){
					//$scope.onViewPanchayatList($scope.stateCode, $scope.stateName, 'gpTemplate', 0);
					$scope.stateName = null;
					$scope.type = 'S';
				}else{
//					$scope.onZpBpNameBpCount($scope.objectDetails, 'gpTemplate', 1);	
					$scope.onZpBpNameBpCount($scope.objectDetails, 'gpTemplate', 1);
				}

			}else if($scope.gpViewTemplateId==3){
				$scope.onBpGpNameBErCount($scope.objectDetails, 'gpTemplate', 2);
			}else{
				$scope.stateName = null;
				$scope.type = 'S';
			}
		}
		
	}
	
	// --on click zp name count of bp 
	$scope.onClickBpCountOn = function onClickBpCountOn(stateId, templateId, obj, viewTemplateId){
		$scope.type = '';
		$scope.loader = true;
		$scope.objectDetails = obj;
		document.getElementById('stateLevel').style.display = 'none';
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = '';
		}
		document.getElementById('displayStateWise').style.display = 'none';
		$scope.stateCode = stateId;
		$scope.stateName = obj.stateName;
		$scope.zpName = obj.zpName;
		if(templateId=='zpTemplate'){
			$scope.zpViewTemplateId = viewTemplateId;
		}else if(templateId=='bpTemplate'){
			$scope.bpViewTemplateId = viewTemplateId;
		}else if(templateId=='gpTemplate'){
			$scope.gpViewTemplateId = viewTemplateId;
		}
		onViewBptListData(stateId, currentYear, templateId, obj);
		
	}
	
	
	
	function onViewBpListData(stateId, currentYear, templateId, object){
		   
		$scope.loader = true;
		$scope.type = 'B';
		$scope.stateName = object.stateName;
		$scope.zpName = object.zpName;
		$scope.detailsData = {};
		$scope.sumTotalZpCount = 0;
		$scope.totalERCount = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;
		
		ElectedService.findPanchayatByStateCode(stateId, currentYear, templateId).then(function(response) {
			if (response.data){
				$scope.data = response.data;
				$scope.detailsData = response.data;
				 angular.forEach($scope.detailsData, function(obj, key) {
	    			if(obj.pcount) {
	    				obj.stateName=object.stateName;
	    				$scope.totalERCount = $scope.totalERCount + obj.count;
	    				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
	    				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
	    				$scope.totalOtherCount = $scope.totalOtherCount + obj.otherCount;
	    			}
		    	});
			} else {
	            console.error("No data received from the API!");
	        }
			$scope.loader = false;
	    });
	}
	// drilthru click on zp name in count bp
	$scope.onClickBpCount = function onClickBpCount(stateId, stateName, templateId, obj){
		$scope.type = '';
		$scope.loader = true;
		document.getElementById('stateLevel').style.display = 'none';
		document.getElementById('displayStateWise').style.display = 'none';
//		document.getElementById('displayBpWiseZp').style.display = 'none';
		$scope.stateCode = stateId;
		$scope.stateName = obj.stateName;
		if(templateId=='zpTemplate'){
			onViewBptListData(stateId, currentYear, templateId, obj);
		}else if(templateId=='bpTemplate'){
			onViewBptListData(stateId, currentYear, templateId, obj);
		}else if(templateId=='gpTemplate'){
			onViewBptListData(stateId, currentYear, templateId, obj);
		}
		
		
	}
	
	function onViewBptListData(stateId, currentYear, templateId, object){
		   
		$scope.loader = true;
		$scope.type = 'B';
		$scope.detailsData = {};
		$scope.sumTotalZpCount = 0;
		$scope.totalERCount = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;
		
		
		ElectedService.findBpByZpCode(stateId, currentYear, templateId, object.zpCode).then(function(response) {
			if (response.data){
				$scope.data = response.data;
				$scope.detailsData = response.data;
				 angular.forEach($scope.detailsData, function(obj, key) {
	    			if(obj.bpCode) {
	    				if(templateId=='zpTemplate'){
	    					
	    				}else if(templateId=='bpTemplate'){
	    					$scope.totalERCount = $scope.totalERCount + obj.bperCount;
	    				}else if(templateId=='gpTemplate'){
	    			
	    				}
	    				obj.stateName=object.stateName;
	    			
	    				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
	    				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
	    				$scope.totalOtherCount = $scope.totalOtherCount + obj.otherCount;
	    			}
		    	});
			} else {
	            console.error("No data received from the API!");
	        }
			$scope.loader = false;
	    });
	}
	
	/** **********************************************/
	$scope.onDistrictCount = function onDistrictCount(stateId, stateName){
		document.getElementById('stateLevel').style.display = 'none';
		$scope.stateCode = stateId;
		$scope.stateName = stateName;
		if(stateId == 13 || stateId == 15 || stateId == 17) {
			document.getElementById('villageLevel').style.display = '';
			if(stateId == 13) {
				villageDetails(12);
			}
			if(stateId == 15) {
				villageDetails(11);
			}
			if(stateId == 17) {
				villageDetails(22)
			}
			$scope.type = 'SGP';
		} else if(stateId == 34){
			document.getElementById('blockCountLevel').style.display = '';
			$scope.type = 'SB';
			getBlockCount(2);
		} else {
			document.getElementById('districtCountLevel').style.display = '';
			getDistrictCount(stateId);
		}
	}
	
	function getDistrictCount(stateId) {
		$scope.loader = true;
		$scope.type = 'D';
		$scope.sumTotalGPCount = 0;
		$scope.totalDistrictCount = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;
	    $scope.details = {};
		ElectedService.findDistrictCountForGP(stateId, $scope.year).then(function(response) {
			$scope.data = response.data;
			var gpProfileDetails = new Array();
			angular.forEach($scope.data, function(obj, key) {
				var gpProfile = new gpCount();
				if(obj.level != null) {
					gpProfile.entityCode = obj.code;
					gpProfile.entityName = obj.name;
					gpProfile.totalGPCount = obj.gpCount;
					gpProfile.count = obj.count + obj.maleCount+ obj.femaleCount;
					
					if(obj.maleCount != null && obj.maleCount !=0 ){
						gpProfile.maleCount = obj.maleCount;
					}else{
						gpProfile.maleCount = 0;
					}
					
					if(obj.femaleCount !=null && obj.femaleCount != 0){
						gpProfile.femaleCount = obj.femaleCount;
					}else{
						gpProfile.femaleCount=0;
					}
					
					if(obj.count !=null && obj.count != 0){
						gpProfile.otherCount = obj.count;
					}else{
						gpProfile.otherCount=0;
					}
					gpProfile.level = obj.level;
					gpProfileDetails.push(gpProfile);
				
					$scope.sumTotalGPCount = $scope.sumTotalGPCount + obj.gpCount;
					$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
					$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
					$scope.totalOtherCount = $scope.totalOtherCount + obj.count;
					$scope.totalDistrictCount = $scope.totalMaleCount + $scope.totalFemaleCount + $scope.totalOtherCount;
				}
			});	
			$scope.details = gpProfileDetails;
			$scope.loader = false;
	    });
	}
	
	$scope.onBlockCount = function onBlockCount(zpId, zpName){
		document.getElementById('stateLevel').style.display = 'none';
		document.getElementById('districtCountLevel').style.display = 'none';
		document.getElementById('blockCountLevel').style.display = '';
		if($scope.stateCode != 34){
			$scope.zpName = zpName;
			$scope.zpCode = zpId;
			$scope.type = 'B';
		}
		getBlockCount(zpId);
	}
	
	function getBlockCount(zpId) {
		$scope.loader = true;
		$scope.sumTotalGPCount = 0;
		$scope.totalBlockCount = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;
		$scope.details = {};
		ElectedService.findBlockCountForGP($scope.stateCode, zpId, $scope.year).then(function(response) {
			$scope.data = response.data;
			var gpProfileDetails = new Array();
			angular.forEach($scope.data, function(obj, key) {
				var gpProfile = new gpCount();
				gpProfile.entityCode = obj.code;
				gpProfile.entityName = obj.name;
				gpProfile.totalGPCount = obj.gpCount;
				gpProfile.level = obj.level;
				gpProfile.count = obj.count + obj.maleCount+ obj.femaleCount;
				
				
				if(obj.maleCount != null && obj.maleCount !=0 ){
					gpProfile.maleCount = obj.maleCount;
				}else{
					gpProfile.maleCount = 0;
				}
				
				if(obj.femaleCount != null && obj.femaleCount !=0){
					gpProfile.femaleCount = obj.femaleCount;
				}else{
					gpProfile.femaleCount = 0;
				}
				
				if(obj.count != null && obj.count != 0){
					gpProfile.otherCount = obj.count;
				}else{
					gpProfile.otherCount=0;
				}
				gpProfileDetails.push(gpProfile);
				
				$scope.sumTotalGPCount = $scope.sumTotalGPCount + obj.gpCount;
				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
				$scope.totalOtherCount= $scope.totalOtherCount + obj.count;
				$scope.totalBlockCount = $scope.totalMaleCount+ $scope.totalFemaleCount + $scope.totalOtherCount;
		});	
			$scope.details = gpProfileDetails;
			$scope.loader = false;
	    });
	}
	
	$scope.onVillage = function onVillage(code, name, type){
		$scope.villcd =code; 
		document.getElementById('stateLevel').style.display = 'none';
		document.getElementById('districtCountLevel').style.display = 'none';
		document.getElementById('blockCountLevel').style.display = 'none';
		document.getElementById('villageLevel').style.display = '';
		if(type == 'D') {
			$scope.zpName = name;
			$scope.type = 'DGP';
		} else {
			$scope.name = name;
			$scope.type = 'BGP';
		}
		villageDetails(code);
	}
	
	function villageDetails(code) {
		$scope.loader = true;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.totalOtherCount = 0;
		$scope.details = {};
		$scope.totalVillageCount = 0;

		ElectedService.findVillageWise($scope.stateCode, code, $scope.year).then(function(response) {
			$scope.data = response.data;
			var gpProfileDetails = new Array();
			angular.forEach($scope.data, function(obj, key) {
				var gpProfile = new gpCount();
				gpProfile.entityCode = obj.code;
				gpProfile.entityName = obj.name;
				gpProfile.count = obj.count + obj.maleCount+ obj.femaleCount;
				
				if(obj.maleCount != null && obj.maleCount !=0){
					gpProfile.maleCount = obj.maleCount;
				}else{
					gpProfile.maleCount = 0;
				}
				
				if(obj.femaleCount != null && obj.femaleCount !=0){
					gpProfile.femaleCount = obj.femaleCount;
				}else{
					gpProfile.femaleCount = 0;
				}
				
				if(obj.count != null && obj.count != 0){
					gpProfile.otherCount = obj.count;
				}else{
					gpProfile.otherCount=0;
				}
				gpProfileDetails.push(gpProfile);
				
				$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
				$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
				$scope.totalOtherCount = $scope.totalOtherCount + obj.count;
				$scope.totalVillageCount =$scope.totalMaleCount + $scope.totalFemaleCount + $scope.totalOtherCount;

			});	
			$scope.details = gpProfileDetails;
			$scope.loader = false;
	    });
	}
	
	$scope.onBack = function(stateCode, type, zpCode) {
		document.getElementById('districtCountLevel').style.display = 'none';
		document.getElementById('blockCountLevel').style.display = 'none';
		document.getElementById('villageLevel').style.display = 'none';
		document.getElementById('stateLevel').style.display = 'none';
		document.getElementById('ElectedLevel').style.display = 'none';

		$scope.sumTotalGPCount = 0;
		$scope.totalDistrictCount = 0;
		$scope.details = {};
		if(type == 'D' || type == 'SB' || type == 'SGP') {
			document.getElementById('stateLevel').style.display = '';
			onBackToState();
		} else if(type=='B'||type == 'DGP') {
			$scope.zpName = null;
			$scope.zpCode = null;
			$scope.type = 'D';
			document.getElementById('districtCountLevel').style.display = '';
			getDistrictCount(stateCode);
		} else if(type == 'BGP') {
			$scope.code = null;
			$scope.name = null;
			document.getElementById('blockCountLevel').style.display = '';
			if(stateCode != 34) {
				$scope.type = 'B';
				getBlockCount(zpCode);
			} else {
				$scope.type = 'SB';
				getBlockCount(2);
			}
		}
		else if(type == 'E')
			{
			$scope.code = null;
			$scope.stateCode = stateCode;
			$scope.villagename = null;
			document.getElementById('villageLevel').style.display = '';
			villageDetails($scope.villcd);
			$scope.type='BGP';
			if($scope.stateCode==11||$scope.stateCode==14||$scope.stateCode==25||$scope.stateCode==26||$scope.stateCode==30||$scope.stateCode==31)
			{
				$scope.type='DGP';
			}
		}
		
	}
	
	function onBackToState () {
		$scope.loader = true;
		$scope.type = 'S';
		$scope.details = {};
		$scope.sumTotalGPCount = 0;
		$scope.totalCount = 0;
		$scope.totalMaleCount = 0;
		$scope.totalFemaleCount = 0;
		$scope.stateCode = null;
		$scope.stateName = null;
		$scope.zpName = null;
		$scope.zpCode = null;
		$scope.code = null;
		$scope.name = null;
		ElectedService.findStateWise($scope.year).then(function(response) {
			$scope.data = response.data;
			var gpProfileDetails = new Array();
			angular.forEach($scope.data, function(obj, key) {
				var gpProfile = new state();
				if(obj.code != 7 && obj.code != 4) {
					gpProfile.stateCode = obj.code;
					gpProfile.stateName = obj.name;
					gpProfile.totalGPCount = obj.gpCount;
					gpProfile.count = obj.count + obj.maleCount+ obj.femaleCount;
					
					if(obj.maleCount != null && obj.maleCount !=0){
						gpProfile.maleCount = obj.maleCount;
					}else{
						gpProfile.maleCount = obj.maleCount;
					}
					
					if(obj.femaleCount != null && obj.femaleCount != 0){
						gpProfile.femaleCount = obj.femaleCount;
					}else{
					gpProfile.femaleCount = 0;
					}
					if(obj.count != null && obj.count != 0){
						gpProfile.otherCount=obj.count;
					}else{
						gpProfile.otherCount = 0;
					}
					gpProfileDetails.push(gpProfile);
				
					$scope.sumTotalGPCount = $scope.sumTotalGPCount + obj.gpCount;
					$scope.totalMaleCount = $scope.totalMaleCount + obj.maleCount;
					$scope.totalFemaleCount = $scope.totalFemaleCount + obj.femaleCount;
					$scope.totalOtherCount = $scope.totalOtherCount + obj.count;
					$scope.totalCount = $scope.totalMaleCount+ $scope.totalFemaleCount + $scope.totalOtherCount;
				}	
			});	
			$scope.details = gpProfileDetails;
			$scope.loader = false;
	    });
	}
	
	$scope.getGPDetails = function getGPDetails(gpCode) {
		window.open("viewGpProfile.do?localBodyCode="+gpCode, '_blank');
	}
	
	$scope.exportFile = function exportFile(id) {
		$("#" + id).excelexportjs({
			containerid : id,
			datatype : 'table',
			worksheetName : "No. of Elected Representatives",
		});
	}

	$scope.onPrint = function onPrint(id) {
		$("#" + id).print({
			addGlobalStyles : false,
			stylesheet : null,
			rejectWindow : true,
			noPrintSelector : ".no-print",
			iframe : true,
			append : null,
			prepend : null,
			title : "No. of Elected Representatives"
		});
	}

	
	$scope.getElectedDetails = function getElectedDetails(code,name) {	
		if(document.getElementById('stateLevel')){
			document.getElementById('stateLevel').style.display = 'none';
		}
		if(document.getElementById('villageLevel')){
			document.getElementById('villageLevel').style.display = 'none';
		}
		if(document.getElementById('districtCountLevel')){
			document.getElementById('districtCountLevel').style.display = 'none';
		}
		if(document.getElementById('blockCountLevel')){
			document.getElementById('blockCountLevel').style.display = 'none';
		}
		if(document.getElementById('displayStateWise')){
			document.getElementById('displayStateWise').style.display = 'none';
		}
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = 'none';
		}
		if(document.getElementById('ElectedLevel')){
			document.getElementById('ElectedLevel').style.display = '';
		}

		$scope.type='E';
		$scope.loader = true;
		$scope.details = {};
		ElectedService.findElectedDetail(code).then(function(response) {
			$scope.data = response.data;
			var ElectedDetails = new Array();
			$scope.villagename = name;
			angular.forEach($scope.data, function(obj, key) {
				var Elected = new gpElectedData();
				Elected.electedName = obj.electedname;
				Elected.designation = obj.designationname;

				Elected.mobNo = obj.mobno;
				Elected.email=obj.emailid;

				ElectedDetails.push(Elected);
			});	
			$scope.details = ElectedDetails;
			$scope.loader = false;
	    });
	}

	
	$scope.getElectedMembers = function getElectedMembers(code, name, templateId, viewTemplateId) {	
		if(document.getElementById('stateLevel')){
			document.getElementById('stateLevel').style.display = 'none';
		}
		if(document.getElementById('villageLevel')){
			document.getElementById('villageLevel').style.display = 'none';
		}
		if(document.getElementById('districtCountLevel')){
			document.getElementById('districtCountLevel').style.display = 'none';
		}
		if(document.getElementById('blockCountLevel')){
			document.getElementById('blockCountLevel').style.display = 'none';
		}
		if(document.getElementById('displayStateWise')){
			document.getElementById('displayStateWise').style.display = 'none';
		}
		if(document.getElementById('displayBpWiseZp')){
			document.getElementById('displayBpWiseZp').style.display = 'none';
		}
		if(document.getElementById('ElectedLevel')){
			document.getElementById('ElectedLevel').style.display = '';
		}
		
		if(templateId=='zpTemplate'){
			$scope.zpViewTemplateId = viewTemplateId;
			$scope.level = 'D';
		}else if(templateId=='bpTemplate'){
			$scope.bpCode = code;
			$scope.bpName = name;
			$scope.bpViewTemplateId = viewTemplateId;
			$scope.level = 'I';
		}else if(templateId=='gpTemplate'){
			$scope.gpViewTemplateId = viewTemplateId;
			$scope.level = 'V';
		}
		
		$scope.type='E';
		$scope.loader = true;
		$scope.details = {};
		ElectedService.findElectedDetail(code,$scope.stateCode,$scope.level).then(function(response) {
			$scope.data = response.data;
			var ElectedDetails = new Array();
			$scope.villagename = name;
			angular.forEach($scope.data, function(obj, key) {
				var Elected = new gpElectedData();
				Elected.electedName = obj.electedname;
				Elected.designation = obj.designationname;

				Elected.mobNo = obj.mobno;
				Elected.email=obj.emailid;

				ElectedDetails.push(Elected);
			});	
			$scope.details = ElectedDetails;
			$scope.loader = false;
	    });
	}
}]);