import mysql.connector
my_conn = mysql.connector.connect(
host="localhost",
user="root",
password="12345",
database="project"
)

Condition=True

while(Condition):

    print()
    print("1.Insert new test data for Prediction")
    print("2.Insert testname with no details for prediction")
    print("3.Prediction for each testname based on Patient id")
    print("4.Exit")

    print()
    ch=int(input("Enter your choice: "))
    print()

    if ch==1:

        bmkn=input("Enter Biomarker_name : ")
        bmkid=int(input("Enter Biomarker_id : "))
        tc=int(input("Enter Test_Code : "))
        g=input("Enter Gender : ")
        mina=float(input("Enter Min Age : "))
        maxa=float(input("Enter Max Age : "))
        stnor=float(input("Enter Starting range of Normal : "))
        endnor=float(input("Enter Ending range of Normal : "))
        stmd=float(input("Enter Starting range of Mildly Decreased : "))
        endmd=float(input("Enter Ending range of Mildly Decreased : "))
        stmi=float(input("Enter Starting range of Mildly Increased : "))
        endmi=float(input("Enter Ending range of Mild Increased : "))
        stsmd=float(input("Enter Starting range of Significantly Decreased : "))
        endsmd=float(input("Enter Ending range of Significantly Decreased : "))
        stsmi=float(input("Enter Starting range of Significantly Increased : "))
        endsmi=float(input("Enter Ending range of Significantly Increased : "))
        unit=input("Enter Unit : ")

        count=0
        cur=my_conn.cursor()
        cur.execute("select count(*) from cmp;")
        co=cur.fetchall()
        gok=co[0]
        count=gok[0]

        cur=my_conn.cursor()
        cur.execute("alter table cmp auto_increment={};".format(count))


        cur = my_conn.cursor()
        cur.execute("insert into cmp values (\"{}\",{},{},\"{}\",{},{},{},{},{},{},{},{},{},{},{},{},\"{}\",0);".format(bmkn,bmkid,tc,g,mina,maxa,stnor,endnor,stmd,stmi,endmd,endmi,stsmd,endsmd,stsmi,endsmi,unit))
        a=cur.fetchall()

        my_conn.commit()

    elif ch==2:
        test_code=[]
        testid=[]

        cur = my_conn.cursor()
        cur.execute("select distinct(test_code) from cmp;")
        cmpres=cur.fetchall()
        for m in cmpres:
            test_code.append(m[0])

        cur = my_conn.cursor()
        cur.execute("select distinct(testid) from ptdt;")
        cmpres=cur.fetchall()
        for m in cmpres:
            testid.append(m[0])
        
        cur = my_conn.cursor()
        cur.execute("delete from missing_test;")
        abc=cur.fetchall()

        test_code.sort()
        testid.sort()

        cur = my_conn.cursor()
        cur.execute("select testid,testname from ptdt where testid not in {};".format(tuple(test_code)))
        abc=cur.fetchall()
        for q in abc:
            cur=my_conn.cursor()
            cur.execute("insert ignore into missing_test values ({},\"{}\");".format(q[0],q[1]))
        my_conn.commit()
        print("Missing values inserted Successfully")
        print()

    elif ch==3:

        patientid = []

        cur = my_conn.cursor()
        cur.execute("select distinct(patientid) from ptdt;")
        a=cur.fetchall()
        for i in  a:
            patientid.append(i[0])

        ptid=int(input("Enter Patient id : "))

        nrmsc=0
        mdsc,misc,sdsc,sisc=0,0,0,0

        if ptid in patientid:

            cur = my_conn.cursor()
            cur.execute("select testid,test_value_numeric,gender,age,testname from ptdt where patientid={};".format(ptid))
            res=cur.fetchall()
            for n in res:
                cur = my_conn.cursor()
                cur.execute("select test_code,gender,maxage,minage,id from cmp where test_code={};".format(n[0]))
                cmpres=cur.fetchall()
                for m in cmpres:
                    if n[0]==m[0]:#check for testid
                        if n[2]==m[1] or m[1]=='both':#check for gender
                            if n[3]>=m[3] and n[3]<=m[2]:#check for age
                                cur = my_conn.cursor()
                                cur.execute("select stnor,endnor,stmd,endmd,stmi,endmi,stsmd,endsmd,stsmi,endsmi from cmp where id={};".format(m[4]))
                                test_res=cur.fetchall()
                                for num in test_res:
                                    if n[1]!=None:
                                        print()
                                        print("Test name = {}".format(n[4]))
                                        print("Test id = {}".format(n[0]))
                                        if n[1]>=num[0] and n[1]<=num[1]:
                                            cur = my_conn.cursor()
                                            cur.execute("update ptdt set test_status='Normal' where patientid={} and testid={};".format(ptid,n[0]))
                                            print("Normal for Patientid = {}".format(ptid))
                                            nrmsc+=1
                                            break

                                        elif n[1]>=num[2] and n[1]<=num[3]:
                                            cur = my_conn.cursor()
                                            cur.execute("update ptdt set test_status='Mildly decreased' where patientid={} and testid={};".format(ptid,n[0]))
                                            print("Mildly decreased for Patientid = {}".format(ptid))
                                            mdsc+=1
                                            break

                                        elif n[1]>=num[4] and n[1]<=num[5]:
                                            cur = my_conn.cursor()
                                            cur.execute("update ptdt set test_status='Mildly increased' where patientid={} and testid={};".format(ptid,n[0]))
                                            print("Mildly Increased for Patientid = {}".format(ptid))
                                            misc+=1
                                            break

                                        elif n[1]>=num[8] and n[1]<=num[9]:
                                            cur = my_conn.cursor()
                                            cur.execute("update ptdt set test_status='Significantly Increased' where patientid={} and testid={};".format(ptid,n[0]))
                                            print("Significantly Increased for Patientid = {}".format(ptid))
                                            sisc+=1
                                            break
                                    
                                        elif n[1]>=num[6] and n[1]<=num[7]:
                                            cur = my_conn.cursor()
                                            cur.execute("update ptdt set test_status='Significantly decreased' where patientid={} and testid={};".format(ptid,n[0]))
                                            print("Significantly decreased for Patientid = {}".format(ptid))
                                            sdsc+=1
                                            break
                                        else:
                                            print("out of range")
                                            cur=my_conn.cursor()
                                            cur.execute("insert ignore into outdata values({},\"{}\",{});".format(n[0],n[4],n[1]))
                                            my_conn.commit()
                                    else:
                                        print("No test value for Patientid = {}".format(ptid))

                            else:
                                cur = my_conn.cursor()
                                cur.execute("select testid,testname from ptdt where patientid={};".format(ptid))
                                ab=cur.fetchall()
                                for l in ab:
                                    cur=my_conn.cursor()
                                    cur.execute("insert ignore into unfit values({},\"age\",{},\"{}\");".format(ptid,l[0],l[1]))
                                my_conn.commit()
                        else:
                            cur = my_conn.cursor()
                            cur.execute("select testid,testname from ptdt where patientid={};".format(ptid))
                            ab=cur.fetchall()
                            for l in ab:
                                cur=my_conn.cursor()
                                cur.execute("insert ignore into unfit values({},\"Gender\",{},\"{}\");".format(ptid,l[0],l[1]))
                            my_conn.commit()

                            

            xaxis=[]
            xaxis.append(nrmsc)
            xaxis.append(mdsc)
            xaxis.append(misc)
            xaxis.append(sdsc)
            xaxis.append(sisc)
            category=['Normal','Mildly Decreased','Mildly Increased','Significantly Decreased','Significantly Increased']

            import matplotlib.pyplot as plt

            '''plt.pie(xaxis,labels=['Normal','Mildly Decreased','Mildly Increased','Significantly Decreased','Significantly Increased'],autopct="%1.1f%%")
            plt.title("Test Scores")
            plt.legend(loc='upper left')
            plt.legend(bbox_to_anchor=(1,1),loc='upper left')
            plt.show()'''

            print("Close the graph to proceed further")

            ax=plt.subplot()
            bars=ax.bar(category,xaxis,width=0.3,color=['Green','Orange','Orange','Red','Red'])
            ax.bar_label(bars)

            plt.title("Test Scores for Patient id {}".format(ptid))
            plt.xlabel("Category")
            plt.ylabel("Score")
            plt.show(block=False)
            plt.pause(30)
            plt.close()
            
        else:
            print()
            print("Invalid Patient id")
            print()

    elif ch==100000:
        print()
        patientid = []

        cur = my_conn.cursor()
        cur.execute("select distinct(patientid) from ptdt;")
        a=cur.fetchall()
        for i in  a:
            patientid.append(i[0])

        ptid=int(input("Enter Patient id : "))

        if ptid in patientid:
            cur = my_conn.cursor()
            cur.execute("select testid,test_value_numeric,gender,age,testname from ptdt where patientid={};".format(ptid))
            res=cur.fetchall()
            for n in res:
                cur = my_conn.cursor()
                cur.execute("select test_code,gender,maxage,minage,id from cmp where test_code={};".format(n[0]))
                cmpres=cur.fetchall()
                for m in cmpres:
                    if n[0]==m[0]:#check for testid
                        if n[2]==m[1] or m[1]=='both':#check for gender
                            if n[3]>=m[3] and n[3]<=m[2]:#check for age
                                continue
                            else:
                                print("Age of the Patient is not matched")
                                cur = my_conn.cursor()
                                cur.execute("select testid,testname from ptdt where patientid={};".format(ptid))
                                ab=cur.fetchall()
                                for l in ab:
                                    cur=my_conn.cursor()
                                    cur.execute("insert ignore into unfit values({},\"age\",{},\"{}\");".format(ptid,l[0],l[1]))    
                            my_conn.commit()

                        else:
                            print("Gender of the Patient is not matched")
                            cur = my_conn.cursor()
                            cur.execute("select testid,testname from ptdt where patientid={};".format(ptid))
                            ab=cur.fetchall()
                            for l in ab:
                                cur=my_conn.cursor()
                                cur.execute("insert ignore into unfit values({},\"Gender\",{},\"{}\");".format(ptid,l[0],l[1]))    
                            my_conn.commit()
                            

        


    elif ch==4:
        Condition=False
        print("Terminated Successfully")
        print()

    else:
        print("Enter valid Choice")
        print()

    