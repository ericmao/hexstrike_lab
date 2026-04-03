"""Tool adapters (nmap, nikto, ...)."""

from hexstrike_lab.adapters.nmap import NmapAdapter
from hexstrike_lab.adapters.nikto import NiktoAdapter

__all__ = ["NmapAdapter", "NiktoAdapter"]
