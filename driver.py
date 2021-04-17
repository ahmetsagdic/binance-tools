# ------------------------------------------------------------------------------
# a test commandline driver to run my scripts.
#
# @Author: Ahmet Sagdic
# @Date: 17/04/2021
# ------------------------------------------------------------------------------
import open_orders

flag=1
while(flag==1):
    inp=input("input:")
    if(inp=='a'):
        print("calling open orders")
        resp=open_orders.get_all_open_orders()
        if(resp!=None):
            print(resp.text)
            print('used weight:',resp.headers['x-mbx-used-weight'])
        else:
            print('null response')
    if(inp=='s'):
        flag=0
        print('cya')