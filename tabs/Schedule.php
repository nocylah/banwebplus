<?php

function init_schedule() {
	return '<table class=\'table_title\'><tr><td>
    <div class=\'centered\'>Selected Classes</div>
</td></tr></table>
<div id=\'schedule_tab_user_schedule\' class=\'centered\'>&nbsp;</div><br />
<table class=\'table_title\'><tr><td>
    <div class=\'centered\'>Recently Selected</div>
</td></tr></table>
<div id=\'schedule_tab_user_recently_viewed_schedule\' class=\'centered\'>&nbsp;</div>
<input type=\'button\' style=\'display:none;\' name=\'onselect\' onclick=\'draw_schedule_tab();\' />';
}

$tab_init_function = 'init_schedule';

?>