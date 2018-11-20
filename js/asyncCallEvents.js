function changePageAsynch(elementName, url)
{
	$.ajax(
		{
			type: "GET",
			url: url,
			error: function (request, error) 
			{
				alert(" Can't do because: " + error);
			},			
			complete:function(data) 
			{
				var element = document.getElementById(elementName);
				element.parentNode.replaceChild($(data.responseText)[0], element);		
			}			
		}
	);	
	return false;
}