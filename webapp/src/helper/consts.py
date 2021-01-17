################################################################
############## Controlling Progress of webapp ##################
################################################################
IS_SYSTEM_UP = True  # By default when we run the app, It's out of access (Note: this is also true when server resets)
N_API_NEEDS_LABELING = 398 * 2
TASKS = [{'name': 'Labeling Phase', 'route': '/labeling', 'level': 0},
         {'name': 'Reviewing Phase', 'route': '/reviewing', 'level': 1}]
CURRENT_TASK = TASKS[0]

###########################################
############## Constants ##################
###########################################
SYSTEM_STATUS_MESSAGE = "Sorry, system status is DOWN. We're probably doing some under the hood improvement.."
javadoc_all_class = [1, 2, 3, 4]
