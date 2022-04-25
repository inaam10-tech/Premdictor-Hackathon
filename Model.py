import pandas as pd
import random as rand

def model():
  #Formatting Data Fram
  df1 = pd.read_csv("teamRankings.csv")
  dfPL = df1[df1["league"] == "Barclays Premier League"]
  dfPL.index = dfPL['name']
  dfPL = dfPL["spi"]
  dfPL = dfPL.to_frame().reset_index()
  dfPL.index = dfPL['name']
  
  team_names = list(dfPL.index)
  
  ##Creating Final Table output DataFrame
  finalTable = pd.DataFrame(team_names, columns = ["Teams"])
  finalTable['Points'] = [0]*20
  finalTable['Wins'] = [0]*20
  finalTable['Losses'] = [0]*20
  finalTable['Draws'] = [0]*20
  finalTable.index = finalTable["Teams"]
  
  numMiracle = 0
  numbreakdown = 0
  numSeasons = 0
  seasonTreshold = 100
  ##Simulation of Games
  while numSeasons < seasonTreshold:
    numSeasons += 1
    for i in team_names:
      for j in team_names:
        team1Score = dfPL.loc[i,"spi"]
        #Home Team Advantage
        team1Score += 5
        team2Score = dfPL.loc[j,"spi"]
        injVal1 = rand.randint(0,100)
        injVal2 = rand.randint(0,100)
        if injVal1 >= 90:
          team1Score -= 20
        elif injVal1 >= 60 & injVal1 < 90:
          team1Score -= 10
        if injVal2 >= 90:
          team2Score -= 20
        elif injVal2 >= 60 & injVal2 < 90:
          team2Score -= 10 
        
  
  
        #Randomizing Adjustment Factors for team 1
        if(team1Score/100 > 0.9):
          upperAJFteam1 = (team1Score/100)
          lowerAJFteam1 = (team1Score/100) - 0.75
        elif((team1Score/100 > 0.8) & (team1Score/100 < 0.9)):
          upperAJFteam1 = (team1Score/100) + 0.1
          lowerAJFteam1 = (team1Score/100) - 0.3
        elif((team1Score/100 > 0.7) & (team1Score/100 < 0.8)):
          upperAJFteam1 = (team1Score/100) + 0.15
          lowerAJFteam1 = (team1Score/100) - 0.15
        elif((team1Score/100 > 0.6) & (team1Score/100 < 0.7)):
          upperAJFteam1 = (team1Score/100) + 0.25
          lowerAJFteam1 = (team1Score/100) - 0.1
        else:
          upperAJFteam1 = (team1Score/100) + 0.6
          lowerAJFteam1 = (team1Score/100)
        
        #Randomizing Adjustment Factors for Team 2
        if(team2Score/100 > 0.9):
          upperAJFteam2 = (team2Score/100)
          lowerAJFteam2 = (team2Score/100) - 0.75
        elif((team2Score/100 > 0.8) & (team2Score/100 < 0.9)):
          upperAJFteam2 = (team2Score/100) + 0.1
          lowerAJFteam2 = (team2Score/100) - 0.3
        elif((team2Score/100 > 0.7) & (team2Score/100 < 0.8)):
          upperAJFteam2 = (team2Score/100) + 0.15
          lowerAJFteam2 = (team2Score/100) - 0.15
        elif((team2Score/100 > 0.6) & (team2Score/100 < 0.7)):
          upperAJFteam2 = (team2Score/100) + 0.25
          lowerAJFteam2 = (team2Score/100) - 0.1
        else:
          upperAJFteam2 = (team2Score/100) + 0.6
          lowerAJFteam2 = (team2Score/100)
        
        #Randomization
        upAJFR1 = upperAJFteam1*100
        lowAJFR1 = lowerAJFteam1*100
        upAJFR2 = upperAJFteam2*100
        lowAJFR2 = lowerAJFteam2*100
        team1Score = team1Score*(rand.randint(round(lowerAJFteam1), round(upperAJFteam1))/100)
        team2Score = team2Score*(rand.randint(round(lowerAJFteam2), round(upperAJFteam2))/100)
  
        #Miracle Factor
        if(team1Score < 0.65):
          if(rand.randint(0,100) <= 7):
            team1Score += 0.2
            numMiracle += 1
        if(team2Score < 0.65):
          if(rand.randint(0,100) <= 7):
            team2Score += 0.2
            numMiracle += 1
        #Breakdown Factor
        if(team1Score > 0.8):
          if(rand.randint(0,100) <= 7):
            team1Score -= 0.2
            numbreakdown += 1
        if(team2Score > 0.8):
          if(rand.randint(0,100) <= 7):
            team2Score -= 0.2
            numbreakdown += 1
        if i == j:
          continue
        else:
          if(abs(team1Score-team2Score))< 0.1:
            finalTable.at[i,"Points"] += 1
            finalTable.at[j,"Points"] += 1
            finalTable.at[i,"Draws"] += 1
            finalTable.at[j,"Draws"] += 1
            continue
          elif ((team1Score>team2Score)):
            finalTable.at[i,"Points"] += 3
            finalTable.at[i,"Wins"] += 1
            finalTable.at[j,"Losses"] += 1
            continue
          elif(team2Score>team1Score):
            finalTable.at[j, "Points"] += 3
            finalTable.at[j,"Wins"] += 1
            finalTable.at[i,"Losses"] += 1
            continue
          
  finalTable["Points"] = finalTable["Points"].div(seasonTreshold).round(0)
  finalTable["Losses"] = finalTable["Losses"].div(seasonTreshold).round(0)
  finalTable["Wins"] = finalTable["Wins"].div(seasonTreshold).round(0)
  finalTable["Draws"] = finalTable["Draws"].div(seasonTreshold).round(0)
  
  finalTable[["Points", "Wins", "Losses", "Draws"]] = finalTable[["Points", "Wins", "Losses", "Draws"]].apply(pd.to_numeric)
  
  finalTableSorted = finalTable.sort_values("Points" ,ascending=False)
  # print(finalTableSorted)
  
  finalTableSorted.to_csv('predictions.csv')
  