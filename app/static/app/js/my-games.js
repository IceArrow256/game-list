function show_game_list(show) {
    var lists = ["my-games-games-inbox", "my-games-games-completed", "my-games-games-paused", "my-games-games-dropped", "my-games-games-planning"]
    lists.forEach(item => document.getElementById(item).style.display = "none");
    document.getElementById(show).style.display = "block";
}