import Price

# Get price from recent packet 

# 2 queues of length 60

# If price is a BID  
  # THEN  
  # If price is ESX  
    # If queue is not full 
      # add to queue
    # Else 
      # call buyOrSell


  # If price is SP 
    # If queue is not full 
      # add to queue  
    # Else 
      # call buyOrSell


def buyOrSell(queue, newval):
  # calculate mean based on queue
  # calculated std
  # calculate z-score
  # if z > 2 == negative value (sell)
  # else if z < -2 == positive value (buy)
  # return buy or sell and which price if so  
  # return 0 if nothing  
