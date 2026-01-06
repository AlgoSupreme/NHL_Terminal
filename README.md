# NHL_Terminal
NHL_Term is a comprehensive Python-based Command Line Interface (CLI) suite built for deep-dive NHL data analysis and game forecasting. By interfacing with the official NHL API via the nhlpy library, the program provides users with real-time statistics, detailed roster breakdowns, and custom-built predictive modeling.
# Core Functionalities
* "Sauced Corsi" Win Probability: Uses a proprietary double Pythagorean expectation algorithm that weighs Shots on Goal (SOG) and historical scoring rates to predict game winners.
* Goalie-Adjusted Expected Goals: Calculates Goalie Adjusted Rates (GAR) by analyzing specific goalie save percentages (filtering for those with $>100$ saves) to provide expected goal floors, averages, and ceilings for daily matchups.
* Team & Player Deep-Dives:
  * Teams: View seasonal records, win percentages, and full rosters.
  * Players: Detailed metrics including Shots per Game, Team Goal Percentage, and Assists per Shot.
  * Goalies: Track seasonal save percentages, shots against, and goals against.Batch Roster Reporting: A dedicated mode to generate a full-team statistical snapshot in a tabular format.
## Quickstart Guide
To get started with NHL_Term, follow these steps using the provided batch scripts:
## 1. First-Time Setup & Launch
If this is your first time running the program, use the installation script. This will automatically install the necessary dependencies (like nhlpy) and launch the application.
* File: nhl_install_and_run.bat
* Action: Double-click this file to initialize the environment and start the NHL Term.
## 2. Standard Launch
Once the requirements are installed, you can skip the setup process and launch the program directly for faster access.
* File: nhl_run.bat
* Action: Double-click this file for daily use to jump straight into the statistics and predictions.
## Technical Requirements
* Language: Python 3.x
* API Wrapper: nhlpy
* OS: Windows (for .bat script compatibility) or Unix-based systems (via terminal)
