{
 "cells": [
  {
   "cell_type": "raw",
   "id": "91a0d272-eef4-468c-a160-3848b404ab36",
   "metadata": {},
   "source": [
    "PyChain Ledger\n",
    "you’ll make the following updates to the provided Python file for this Challenge, which already contains the basic `PyChain` ledger structure that you created throughout the module:\n",
    "\n",
    "Step 1: Create a Record Data Class \n",
    "Create a new data class named `Record`. This class will serve as the blueprint for the financial transaction records that the blocks of the ledger will store.\n",
    "\n",
    "Step 2: Modify the Existing Block Data Class to Store Record Data\n",
    "Change the existing `Block` data class by replacing the generic `data` attribute with a `record` attribute that’s of type `Record`.\n",
    "\n",
    "Step 3: Add Relevant User Inputs to the Streamlit Interface\n",
    "Create additional user input areas in the Streamlit application. These input areas should collect the relevant information for each financial record that you’ll store in the `PyChain` ledger.\n",
    "\n",
    "Step 4: Test the PyChain Ledger by Storing Records\n",
    "Test your complete `PyChain` ledger."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "5a7d009a-0594-463d-bda0-e51309723b86",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Imports\n",
    "import streamlit as st\n",
    "from dataclasses import dataclass\n",
    "from typing import Any, List\n",
    "import datetime as datetime\n",
    "import pandas as pd\n",
    "import hashlib"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "aa4bf1e2-3d85-4424-bfa6-e52131c43199",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Step 1: Create a Record Data Class\n",
    "# Define a new Python data class named `Record` to represent financial transaction records.\n",
    "\n",
    "@dataclass\n",
    "class Record:\n",
    "    sender: str\n",
    "    receiver: str\n",
    "    amount: float"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "a65acaac-833e-4730-ab75-3b12947d9ad5",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Step 2: Modify the Existing Block Data Class to Store Record Data\n",
    "@dataclass\n",
    "class Block:\n",
    "    record: Record\n",
    "    creator_id: int\n",
    "    prev_hash: str = \"0\"\n",
    "    timestamp: str = datetime.datetime.utcnow().strftime(\"%H:%M:%S\")\n",
    "    nonce: int = 0\n",
    "\n",
    "    def hash_block(self):\n",
    "        sha = hashlib.sha256()\n",
    "\n",
    "        record = str(self.record).encode()\n",
    "        sha.update(record)\n",
    "\n",
    "        creator_id = str(self.creator_id).encode()\n",
    "        sha.update(creator_id)\n",
    "\n",
    "        timestamp = str(self.timestamp).encode()\n",
    "        sha.update(timestamp)\n",
    "\n",
    "        prev_hash = str(self.prev_hash).encode()\n",
    "        sha.update(prev_hash)\n",
    "\n",
    "        nonce = str(self.nonce).encode()\n",
    "        sha.update(nonce)\n",
    "\n",
    "        return sha.hexdigest()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "ecebe7af-0ed8-494c-93bd-da1b43ed1b22",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Step 3: Define the PyChain Class\n",
    "class PyChain:\n",
    "    def __init__(self, chain: List[Block], difficulty: int = 4):\n",
    "        self.chain = chain\n",
    "        self.difficulty = difficulty\n",
    "\n",
    "    def proof_of_work(self, block):\n",
    "        calculated_hash = block.hash_block()\n",
    "        num_of_zeros = \"0\" * self.difficulty\n",
    "\n",
    "        while not calculated_hash.startswith(num_of_zeros):\n",
    "            block.nonce += 1\n",
    "            calculated_hash = block.hash_block()\n",
    "\n",
    "        print(\"Winning Hash\", calculated_hash)\n",
    "        return block\n",
    "\n",
    "    def add_block(self, candidate_block):\n",
    "        block = self.proof_of_work(candidate_block)\n",
    "        self.chain += [block]\n",
    "\n",
    "    def is_valid(self):\n",
    "        block_hash = self.chain[0].hash_block()\n",
    "\n",
    "        for block in self.chain[1:]:\n",
    "            if block_hash != block.prev_hash:\n",
    "                print(\"Blockchain is invalid!\")\n",
    "                return False\n",
    "\n",
    "            block_hash = block.hash_block()\n",
    "\n",
    "        print(\"Blockchain is Valid\")\n",
    "        return True\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "915a0f35-def6-426f-a687-e082dd890f7e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Step 4: Define the Streamlit Application\n",
    "def main():\n",
    "    st.markdown(\"# PyChain\")\n",
    "    st.markdown(\"## Store a Transaction Record in the PyChain\")\n",
    "\n",
    "    sender = st.text_input(\"Sender\")\n",
    "    receiver = st.text_input(\"Receiver\")\n",
    "    amount = st.number_input(\"Amount\")\n",
    "\n",
    "    if st.button(\"Add Block\"):\n",
    "        new_record = Record(sender=sender, receiver=receiver, amount=amount)\n",
    "        new_block = Block(record=new_record, creator_id=42, prev_hash=pychain.chain[-1].hash_block())\n",
    "        pychain.add_block(new_block)\n",
    "        st.balloons()\n",
    "\n",
    "    pychain_df = pd.DataFrame(pychain.chain).astype(str)\n",
    "    st.write(pychain_df)\n",
    "\n",
    "    difficulty = st.sidebar.slider(\"Block Difficulty\", 1, 5, 2)\n",
    "    pychain.difficulty = difficulty\n",
    "\n",
    "    st.sidebar.write(\"# Block Inspector\")\n",
    "    selected_block = st.sidebar.selectbox(\n",
    "        \"Which block would you like to see?\", pychain.chain\n",
    "    )\n",
    "\n",
    "    st.sidebar.write(selected_block)\n",
    "\n",
    "    if st.button(\"Validate Chain\"):\n",
    "        st.write(pychain.is_valid())\n",
    "\n",
    "# Initialize PyChain\n",
    "pychain = PyChain([Block(record=Record(\"Genesis\", \"Genesis\", 0), creator_id=0)])\n",
    "\n",
    "# Run the Streamlit application\n",
    "if __name__ == \"__main__\":\n",
    "    main()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
