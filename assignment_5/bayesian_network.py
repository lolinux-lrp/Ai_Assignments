"""
Bayesian Network Implementation using pgmpy.

This script demonstrates modeling, problem representation, and inferencing 
using the classic "Alarm Network" (Judea Pearl).

Dependencies:
    pip install pgmpy
"""

try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
except ImportError:
    print("Error: The 'pgmpy' library is required.")
    print("Please install it using: pip install pgmpy")
    exit(1)

def create_alarm_network():
    """
    Creates the Bayesian Network for the Alarm problem.
    Variables:
        - Burglary (B): 0=False, 1=True
        - Earthquake (E): 0=False, 1=True
        - Alarm (A): 0=False, 1=True
        - JohnCalls (J): 0=False, 1=True
        - MaryCalls (M): 0=False, 1=True
    """
    # 1. Define the structure (edges)
    model = BayesianNetwork([
        ('Burglary', 'Alarm'), 
        ('Earthquake', 'Alarm'),
        ('Alarm', 'JohnCalls'),
        ('Alarm', 'MaryCalls')
    ])

    # 2. Define Conditional Probability Distributions (CPDs)
    
    # P(Burglary)
    # [P(B=False), P(B=True)]
    cpd_b = TabularCPD(variable='Burglary', variable_card=2, values=[[0.999], [0.001]])
    
    # P(Earthquake)
    # [P(E=False), P(E=True)]
    cpd_e = TabularCPD(variable='Earthquake', variable_card=2, values=[[0.998], [0.002]])
    
    # P(Alarm | Burglary, Earthquake)
    # Columns correspond to combinations of [Burglary, Earthquake] evidence
    # Combinations: (F,F), (F,T), (T,F), (T,T)
    cpd_a = TabularCPD(
        variable='Alarm', 
        variable_card=2, 
        values=[
            [0.999, 0.71, 0.06, 0.05], # P(A=False)
            [0.001, 0.29, 0.94, 0.95]  # P(A=True)
        ],
        evidence=['Burglary', 'Earthquake'],
        evidence_card=[2, 2]
    )
                       
    # P(JohnCalls | Alarm)
    # Columns correspond to [Alarm=False, Alarm=True]
    cpd_j = TabularCPD(
        variable='JohnCalls', 
        variable_card=2,
        values=[
            [0.95, 0.10], # P(J=False)
            [0.05, 0.90]  # P(J=True)
        ],
        evidence=['Alarm'], 
        evidence_card=[2]
    )
                       
    # P(MaryCalls | Alarm)
    # Columns correspond to [Alarm=False, Alarm=True]
    cpd_m = TabularCPD(
        variable='MaryCalls', 
        variable_card=2,
        values=[
            [0.99, 0.30], # P(M=False)
            [0.01, 0.70]  # P(M=True)
        ],
        evidence=['Alarm'], 
        evidence_card=[2]
    )

    # 3. Add CPDs to the model
    model.add_cpds(cpd_b, cpd_e, cpd_a, cpd_j, cpd_m)
    
    # 4. Verify the model is valid
    assert model.check_model()
    
    return model

def test_inference():
    print("=== Bayesian Network Inference on Alarm Network ===")
    print("0 = False, 1 = True\n")
    
    model = create_alarm_network()
    infer = VariableElimination(model)
    
    # Query 1: Probability of Burglary if John and Mary both call
    print("Query 1: P(Burglary | JohnCalls=1, MaryCalls=1)")
    print("If both neighbors call, what is the probability a burglary actually occurred?")
    q1 = infer.query(variables=['Burglary'], evidence={'JohnCalls': 1, 'MaryCalls': 1})
    print(q1)
    
    # Query 2: Probability of Alarm if there's an Earthquake but no Burglary
    print("\nQuery 2: P(Alarm | Burglary=0, Earthquake=1)")
    q2 = infer.query(variables=['Alarm'], evidence={'Burglary': 0, 'Earthquake': 1})
    print(q2)
    
    # Query 3: Probability of John calling given a Burglary occurred
    print("\nQuery 3: P(JohnCalls | Burglary=1)")
    q3 = infer.query(variables=['JohnCalls'], evidence={'Burglary': 1})
    print(q3)
    
    # Query 4: Explaining Away (Berkson's Paradox)
    # If the alarm goes off, probability of Earthquake:
    q4_a = infer.query(variables=['Earthquake'], evidence={'Alarm': 1})
    print("\nQuery 4a: P(Earthquake | Alarm=1)")
    print(q4_a)
    
    # If the alarm goes off AND we know a Burglary happened, probability of Earthquake drops:
    q4_b = infer.query(variables=['Earthquake'], evidence={'Alarm': 1, 'Burglary': 1})
    print("\nQuery 4b: P(Earthquake | Alarm=1, Burglary=1)  [Notice how the probability decreases]")
    print(q4_b)


if __name__ == "__main__":
    test_inference()
