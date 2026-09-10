"""Command-line browser and exporter for generated content packs."""
import argparse
import csv
import html
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

from flows.library_flow import browse_library