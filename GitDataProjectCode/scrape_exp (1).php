<?php
include_once('simple_html_dom.php');
include_once('csvutil.php');

function getArticleInfo( $month_page, & $ret )
{
	if( empty( $month_page ) )
		return;
		
	$html = str_get_html( $month_page );
	foreach($html->find("article") as $article)
	{
		$url = $article->find("h1 a",0)->href;
		$title = html_entity_decode( $article->find("h1 a",0)->plaintext );
		$date = trim( $article->find(".postmeta p", 2)->plaintext );
		
		$first = explode( " ", $article->find(".postmeta p", 3)->find('text',1) )[0];
		if( $first == "One" )
			$first = "1";
		$comments = $first;
		
		$line = array( $date, $title, $comments );
		$ret[] = $line;
	}
	
    // clean up memory
    /*
   	$html->clear();
   	unset($html);
    */
}

/*
$month_page = file_get_contents("monthpage.html");
$ret = array();
getArticleInfo( $month_page, $ret );
foreach( $ret as $line )
	echo sputcsv( $line );
*/

/*
for( $year = 2006; $year <= $2015; $year++ )
{
	for( $month = 1; $month < 12; $month++ )
}
*/

function getArchiveMonths()
{
return array( 
"2015/04",
"2015/03", 
"2015/02", 
"2015/01", 
"2014/12", 
"2014/11", 
"2014/10", 
"2014/09", 
"2014/08", 
"2014/07", 
"2014/06", 
"2014/05", 
"2014/04", 
"2014/03", 
"2014/02", 
"2014/01", 
"2013/12", 
"2013/11", 
"2013/10", 
"2013/09", 
"2013/08", 
"2013/07", 
"2013/06", 
"2013/05", 
"2013/04", 
"2013/03", 
"2013/02", 
"2013/01", 
"2012/12", 
"2012/11", 
"2012/10", 
"2012/09", 
"2012/08", 
"2012/07", 
"2012/06", 
"2012/05", 
"2012/04", 
"2012/03", 
"2012/02", 
"2012/01", 
"2011/12", 
"2011/11", 
"2011/10", 
"2011/09", 
"2011/08", 
"2011/07", 
"2011/06", 
"2011/05", 
"2011/04", 
"2011/03", 
"2011/02", 
"2011/01", 
"2010/12", 
"2010/11", 
"2010/10", 
"2010/09", 
"2010/08", 
"2010/07", 
"2010/06", 
"2010/05", 
"2010/04", 
"2010/03", 
"2010/02", 
"2010/01", 
"2009/12", 
"2009/11", 
"2009/10", 
"2009/09", 
"2009/08", 
"2009/07", 
"2009/06", 
"2009/05", 
"2009/04", 
"2009/03", 
"2009/02", 
"2009/01", 
"2008/12", 
"2008/11", 
"2008/10", 
"2008/09", 
"2008/08", 
"2008/07", 
"2008/06", 
"2008/05", 
"2008/04", 
"2008/03", 
"2008/02", 
"2008/01", 
"2007/12", 
"2007/11", 
"2007/10", 
"2007/09", 
"2007/08", 
"2007/07", 
"2007/06", 
"2007/05", 
"2007/04", 
"2007/03", 
"2007/02",
"2007/01",
"2006/12",
"2006/11",
"2006/10",
"2006/09",
"2006/08",
"2006/07",
"2006/06",
"2006/05",
"2006/04",
"2006/03",
"2006/02",
"2006/01" );
}

function urlByPostfix( $postfix, $page )
{
	if( $page == 1 )
		return "http://www.the-exponent.com/" . $postfix;
	else
		return "http://www.the-exponent.com/" . $postfix . "/page/" . $page . "/";
}

function fileByPostfix( $postfix, $page )
{
	$clean_postfix = str_replace('/', '', $postfix);
	return "exp/exponent" . $clean_postfix . "_" . $page . ".html";
}

function downloadByPostfix( $postfix )
{
	$page = 0;
	while( true )
	{
		$page++;
		$url = urlByPostfix( $postfix, $page );
		$filename = fileByPostfix( $postfix, $page );
		echo "Trying to get $url\n";
		$src = file_get_contents( $url );
		if( empty( $src ) )
		{
			echo "Next month\n";
			break;
		}
		//sleep( 0.5 );
		echo "Trying to write file $filename\n";
		file_put_contents( $filename, $src );
	}
}

function extractByPostfix( $postfix, & $ret )
{
	$page = 0;
	while( true )
	{
		$page++;
		$filename = fileByPostfix( $postfix, $page );
		if( !file_exists( $filename ) )
			break;
		//echo "Extracting from $filename\n";
		$src = file_get_contents( $filename );
		if( empty($src) )
		{
			echo "Next month\n";
			break;
		}
		getArticleInfo( $src, $ret );
	}
}

$postfixes = getArchiveMonths();
foreach( $postfixes as $postfix )
{
	$ret = array();

	if( false )
	{
		downloadByPostfix( $postfix );
	}
	else
	{
		extractByPostfix( $postfix, $ret );

		foreach( $ret as $line )
			echo sputcsv( $line );
	}
}

?>